# -*- coding: utf-8 -*-

import collections
import gc
from typing import Union, Dict, Callable, Sequence, Optional, Tuple

import jax
import jax.numpy as jnp
import numpy as np

from brainpy import tools
from brainpy._src import math as bm
from brainpy._src.connect import TwoEndConnector, MatConn, IJConn, One2One, All2All
from brainpy._src.initialize import Initializer, parameter, variable, Uniform, noise as init_noise
from brainpy._src.integrators import odeint, sdeint
from brainpy._src.math.object_transform.variables import Variable, VariableView
from brainpy._src.math.object_transform.base import BrainPyObject, Collector
from brainpy.errors import NoImplementationError, UnsupportedError
from brainpy.types import ArrayType, Shape

share = None

__all__ = [
  # general class
  'DynamicalSystem',
  'DynamicalSystemNS',

  # containers
  'Container', 'Network', 'Sequential', 'System',

  # channel models
  'Channel',

  # neuron models
  'NeuGroup', 'CondNeuGroup', 'NeuGroupNS',

  # synapse models
  'SynConn',
  'TwoEndConn',
  'SynOut', 'NullSynOut',
  'SynSTP',
  'SynLTP',

  # slice
  'DSView', 'NeuGroupView',
]

SLICE_VARS = 'slice_vars'


def not_pass_shared(func: Callable):
  """Label the update function as the one without passing shared arguments.

  The original update function explicitly requires shared arguments at the first place::

    class TheModel(DynamicalSystem):
        def update(self, s, x):
            # s is the shared arguments, like `t`, `dt`, etc.
            pass

  So, each time we call the model we should provide shared arguments into the model::

    TheModel()(shared, inputs)

  When we label the update function as ``do_not_pass_sha_args``, this time there is no
  need to call the dynamical system with shared arguments::

    class NewModel(DynamicalSystem):
       @no_shared
       def update(self, x):
         pass

    NewModel()(inputs)

  .. versionadded:: 2.3.5

  Parameters
  ----------
  func: Callable
    The function in the :py:class:`~.DynamicalSystem`.

  Returns
  -------
  func: Callable
    The wrapped function for the class.
  """
  func._new_style = True
  return func


class DynamicalSystem(BrainPyObject):
  """Base Dynamical System class.

  .. note::
     In general, every instance of :py:class:`~.DynamicalSystem` implemented in
     BrainPy only defines the evolving function at each time step :math:`t`.

     Each subclass of :py:class:`~.DynamicalSystem` may have multiple step functions.
     For instance, all our implemented neuron model define two step functions:

     - ``.update()`` for the logic updating
     - ``clear_input()`` for clear all accumulated inputs at this time step.

     If users want to define the logic of running models across multiple steps,
     we recommend users to use :py:func:`~.for_loop`, :py:class:`~.LoopOverTime`,
     :py:class:`~.DSRunner`, or :py:class:`~.DSTrainer`.

  Parameters
  ----------
  name : optional, str
    The name of the dynamical system.
  mode: optional, Mode
    The model computation mode. It should be instance of :py:class:`~.Mode`.
  """

  supported_modes: Optional[Sequence[bm.Mode]] = None
  '''Supported computing modes.'''

  _pass_shared_args: bool = True

  global_delay_data: Dict[str, Tuple[Union[bm.LengthDelay, None], Variable]] = dict()
  '''Global delay data, which stores the delay variables and corresponding delay targets. 
  This variable is useful when the same target variable is used in multiple mappings, 
  as it can reduce the duplicate delay variable registration.'''

  def __init__(
      self,
      name: Optional[str] = None,
      mode: Optional[bm.Mode] = None,
  ):
    # mode setting
    mode = bm.get_mode() if mode is None else mode
    if not isinstance(mode, bm.Mode):
      raise ValueError(f'Should be instance of {bm.Mode.__name__}, '
                       f'but we got {type(mode)}: {mode}')
    self._mode = mode

    if self.supported_modes is not None:
      if not self.mode.is_parent_of(*self.supported_modes):
        raise UnsupportedError(f'The mode only supports computing modes '
                               f'which are parents of {self.supported_modes}, '
                               f'but we got {self.mode}.')

    # local delay variables
    self.local_delay_vars: Dict[str, bm.LengthDelay] = Collector()

    # super initialization
    BrainPyObject.__init__(self, name=name)

  @property
  def mode(self) -> bm.Mode:
    """Mode of the model, which is useful to control the multiple behaviors of the model."""
    return self._mode

  @mode.setter
  def mode(self, value):
    if not isinstance(value, bm.Mode):
      raise ValueError(f'Must be instance of {bm.Mode.__name__}, '
                       f'but we got {type(value)}: {value}')
    self._mode = value

  def __repr__(self):
    return f'{self.__class__.__name__}(name={self.name}, mode={self.mode})'

  def __call__(self, *args, **kwargs):
    """The shortcut to call ``update`` methods."""
    global share
    if share is None:
      from brainpy._src.context import share

    try:
      if self._pass_shared_args:
        if hasattr(self.update, '_new_style') and getattr(self.update, '_new_style'):
          if len(args) and isinstance(args[0], dict):
            share.save(**args[0])
            return self.update(*args[1:], **kwargs)
          else:
            return self.update(*args, **kwargs)
        else:
          if len(args) and isinstance(args[0], dict):
            return self.update(*args, **kwargs)
          else:
            # If first argument is not shared argument,
            # we should get the shared arguments from the global context.
            # However, users should set and update shared arguments
            # in the global context when using this mode.
            return self.update(share.get_shargs(), *args, **kwargs)
      else:
        if len(args) and isinstance(args[0], dict):  # it may be shared arguments
          share.save(**args[0])
          return self.update(*args[1:], **kwargs)
        else:
          return self.update(*args, **kwargs)
    except Exception as e:
      raise RuntimeError(f'Error occurs when running {self.name}: {self}') from e

  def register_delay(
      self,
      identifier: str,
      delay_step: Optional[Union[int, ArrayType, Callable, Initializer]],
      delay_target: Variable,
      initial_delay_data: Union[Initializer, Callable, ArrayType, float, int, bool] = None,
  ):
    """Register delay variable.

    Parameters
    ----------
    identifier: str
      The delay variable name.
    delay_step: Optional, int, ArrayType, callable, Initializer
      The number of the steps of the delay.
    delay_target: Variable
      The target variable for delay.
    initial_delay_data: float, int, ArrayType, callable, Initializer
      The initializer for the delay data.

    Returns
    -------
    delay_step: int, ArrayType
      The number of the delay steps.
    """
    # delay steps
    if delay_step is None:
      delay_type = 'none'
    elif isinstance(delay_step, (int, np.integer, jnp.integer)):
      delay_type = 'homo'
    elif isinstance(delay_step, (bm.ndarray, jnp.ndarray, np.ndarray)):
      if delay_step.size == 1 and delay_step.ndim == 0:
        delay_type = 'homo'
      else:
        delay_type = 'heter'
        delay_step = bm.asarray(delay_step)
    elif callable(delay_step):
      delay_step = parameter(delay_step, delay_target.shape, allow_none=False)
      delay_type = 'heter'
    else:
      raise ValueError(f'Unknown "delay_steps" type {type(delay_step)}, only support '
                       f'integer, array of integers, callable function, brainpy.init.Initializer.')
    if delay_type == 'heter':
      if delay_step.dtype not in [bm.int32, bm.int64]:
        raise ValueError('Only support delay steps of int32, int64. If your '
                         'provide delay time length, please divide the "dt" '
                         'then provide us the number of delay steps.')
      if delay_target.shape[0] != delay_step.shape[0]:
        raise ValueError(f'Shape is mismatched: {delay_target.shape[0]} != {delay_step.shape[0]}')
    if delay_type != 'none':
      max_delay_step = int(bm.max(delay_step))

    # delay target
    if delay_type != 'none':
      if not isinstance(delay_target, Variable):
        raise ValueError(f'"delay_target" must be an instance of Variable, but we got {type(delay_target)}')

    # delay variable
    if delay_type != 'none':
      if identifier not in self.global_delay_data:
        delay = bm.LengthDelay(delay_target, max_delay_step, initial_delay_data)
        self.global_delay_data[identifier] = (delay, delay_target)
        self.local_delay_vars[identifier] = delay
      else:
        delay = self.global_delay_data[identifier][0]
        if delay is None:
          delay = bm.LengthDelay(delay_target, max_delay_step, initial_delay_data)
          self.global_delay_data[identifier] = (delay, delay_target)
          self.local_delay_vars[identifier] = delay
        elif delay.num_delay_step - 1 < max_delay_step:
          self.global_delay_data[identifier][0].reset(delay_target, max_delay_step, initial_delay_data)
    else:
      if identifier not in self.global_delay_data:
        self.global_delay_data[identifier] = (None, delay_target)
    self.register_implicit_nodes(self.local_delay_vars)
    return delay_step

  def get_delay_data(
      self,
      identifier: str,
      delay_step: Optional[Union[int, bm.Array, jax.Array]],
      *indices: Union[int, slice, bm.Array, jax.Array],
  ):
    """Get delay data according to the provided delay steps.

    Parameters
    ----------
    identifier: str
      The delay variable name.
    delay_step: Optional, int, ArrayType
      The delay length.
    indices: optional, int, slice, ArrayType
      The indices of the delay.

    Returns
    -------
    delay_data: ArrayType
      The delay data at the given time.
    """
    if delay_step is None:
      return self.global_delay_data[identifier][1].value

    if identifier in self.global_delay_data:
      if bm.ndim(delay_step) == 0:
        return self.global_delay_data[identifier][0](delay_step, *indices)
      else:
        if len(indices) == 0:
          indices = (bm.arange(delay_step.size),)
        return self.global_delay_data[identifier][0](delay_step, *indices)

    elif identifier in self.local_delay_vars:
      if bm.ndim(delay_step) == 0:
        return self.local_delay_vars[identifier](delay_step)
      else:
        if len(indices) == 0:
          indices = (bm.arange(delay_step.size),)
        return self.local_delay_vars[identifier](delay_step, *indices)

    else:
      raise ValueError(f'{identifier} is not defined in delay variables.')

  def update(self, *args, **kwargs):
    """The function to specify the updating rule.

    Assume any dynamical system depends on the shared variables (`sha`),
    like time variable ``t``, the step precision ``dt``, and the time step `i`.
    """
    raise NotImplementedError('Must implement "update" function by subclass self.')

  def reset(self, *args, **kwargs):
    """Reset function which reset the whole variables in the model.
    """
    self.reset_state(*args, **kwargs)

  def reset_state(self, *args, **kwargs):
    """Reset function which reset the states in the model.
    """
    child_nodes = self.nodes(level=1, include_self=False).subset(DynamicalSystem).unique()
    if len(child_nodes) > 0:
      for node in child_nodes.values():
        node.reset_state(*args, **kwargs)
      self.reset_local_delays(child_nodes)
    else:
      raise NotImplementedError('Must implement "reset_state" function by subclass self. '
                                f'Error of {self.name}')

  def update_local_delays(self, nodes: Union[Sequence, Dict] = None):
    """Update local delay variables.

    This function should be called after updating neuron groups or delay sources.
    For example, in a network model,


    Parameters
    ----------
    nodes: sequence, dict
      The nodes to update their delay variables.
    """
    # update delays
    if nodes is None:
      nodes = tuple(self.nodes(level=1, include_self=False).subset(DynamicalSystem).unique().values())
    elif isinstance(nodes, DynamicalSystem):
      nodes = (nodes,)
    elif isinstance(nodes, dict):
      nodes = tuple(nodes.values())
    if not isinstance(nodes, (tuple, list)):
      raise ValueError('Please provide nodes as a list/tuple/dict of DynamicalSystem.')
    for node in nodes:
      for name in node.local_delay_vars:
        delay = self.global_delay_data[name][0]
        target = self.global_delay_data[name][1]
        delay.update(target.value)

  def reset_local_delays(self, nodes: Union[Sequence, Dict] = None):
    """Reset local delay variables.

    Parameters
    ----------
    nodes: sequence, dict
      The nodes to Reset their delay variables.
    """
    # reset delays
    if nodes is None:
      nodes = self.nodes(level=1, include_self=False).subset(DynamicalSystem).unique().values()
    elif isinstance(nodes, dict):
      nodes = nodes.values()
    for node in nodes:
      for name in node.local_delay_vars:
        delay = self.global_delay_data[name][0]
        target = self.global_delay_data[name][1]
        delay.reset(target.value)

  def __del__(self):
    """Function for handling `del` behavior.

    This function is used to pop out the variables which registered in global delay data.
    """
    if hasattr(self, 'local_delay_vars'):
      for key in tuple(self.local_delay_vars.keys()):
        val = self.global_delay_data.pop(key)
        del val
        val = self.local_delay_vars.pop(key)
        del val
    if hasattr(self, 'implicit_nodes'):
      for key in tuple(self.implicit_nodes.keys()):
        del self.implicit_nodes[key]
    if hasattr(self, 'implicit_vars'):
      for key in tuple(self.implicit_vars.keys()):
        del self.implicit_vars[key]
    for key in tuple(self.__dict__.keys()):
      del self.__dict__[key]
    gc.collect()

  def clear_input(self):
    pass

  def __rrshift__(self, other):
    """Support using right shift operator to call modules.

    Examples
    --------

    >>> import brainpy as bp
    >>> x = bp.math.random.rand((10, 10))
    >>> l = bp.layers.Activation(bm.tanh)
    >>> y = x >> l

    """
    return self.__call__(other)


class Container(DynamicalSystem):
  """Container object which is designed to add other instances of DynamicalSystem.

  Parameters
  ----------
  name : str, optional
    The object name.
  mode: Mode
    The mode which controls the model computation.
  must_be_dynsys_subclass: bool
    Child classes must be the subclass of :py:class:`DynamicalSystem`.
  """

  def __init__(
      self,
      *dynamical_systems_as_tuple,
      name: str = None,
      mode: bm.Mode = None,
      must_be_dynsys_subclass: bool = True,
      **dynamical_systems_as_dict
  ):
    super(Container, self).__init__(name=name, mode=mode)

    if must_be_dynsys_subclass:
      parent = DynamicalSystem
      parent_name = DynamicalSystem.__name__
    else:
      parent = bm.BrainPyObject
      parent_name = bm.BrainPyObject.__name__

    # add tuple-typed components
    for module in dynamical_systems_as_tuple:
      if isinstance(module, parent):
        self.implicit_nodes[module.name] = module
      elif isinstance(module, (list, tuple)):
        for m in module:
          if not isinstance(m, parent):
            raise ValueError(f'Should be instance of {parent_name}. '
                             f'But we got {type(m)}')
          self.implicit_nodes[m.name] = m
      elif isinstance(module, dict):
        for k, v in module.items():
          if not isinstance(v, parent):
            raise ValueError(f'Should be instance of {parent_name}. '
                             f'But we got {type(v)}')
          self.implicit_nodes[k] = v
      else:
        raise ValueError(f'Cannot parse sub-systems. They should be {parent_name} '
                         f'or a list/tuple/dict of {parent_name}.')
    # add dict-typed components
    for k, v in dynamical_systems_as_dict.items():
      if not isinstance(v, parent):
        raise ValueError(f'Should be instance of {parent_name}. '
                         f'But we got {type(v)}')
      self.implicit_nodes[k] = v

  def __repr__(self):
    cls_name = self.__class__.__name__
    indent = ' ' * len(cls_name)
    child_str = [tools.repr_context(repr(val), indent) for val in self.implicit_nodes.values()]
    string = ", \n".join(child_str)
    return f'{cls_name}({string})'

  def update(self, tdi, *args, **kwargs):
    """Update function of a container.

    In this update function, the update functions in children systems are
    iteratively called.

    Parameters
    ----------
    tdi: dict
      The shared arguments including `t` the time, `dt` the time step, `t` the running index.
    """
    nodes = self.nodes(level=1, include_self=False).subset(DynamicalSystem).unique()
    for node in nodes.values():
      node(tdi)

  def __getitem__(self, item):
    """Overwrite the slice access (`self['']`). """
    if item in self.implicit_nodes:
      return self.implicit_nodes[item]
    else:
      raise ValueError(f'Unknown item {item}, we only found {list(self.implicit_nodes.keys())}')

  def __getattr__(self, item):
    """Overwrite the dot access (`self.`). """
    child_ds = super(Container, self).__getattribute__('implicit_nodes')
    if item in child_ds:
      return child_ds[item]
    else:
      return super(Container, self).__getattribute__(item)

  def clear_input(self):
    """Clear inputs in the children classes."""
    for node in self.nodes(level=1, include_self=False).subset(DynamicalSystem).unique().values():
      node.clear_input()



class Network(Container):
  """Base class to model network objects, an alias of Container.

  Network instantiates a network, which is aimed to load
  neurons, synapses, and other brain objects.

  Parameters
  ----------
  name : str, Optional
    The network name.
  monitors : optional, list of str, tuple of str
    The items to monitor.
  ds_tuple :
    A list/tuple container of dynamical system.
  ds_dict :
    A dict container of dynamical system.
  """

  def __init__(
      self,
      *ds_tuple,
      name: str = None,
      mode: bm.Mode = None,
      **ds_dict
  ):
    super(Network, self).__init__(*ds_tuple, name=name, mode=mode, **ds_dict)

  @not_pass_shared
  def update(self, *args, **kwargs):
    """Step function of a network.

    In this update function, the update functions in children systems are
    iteratively called.
    """
    nodes = self.nodes(level=1, include_self=False)
    nodes = nodes.subset(DynamicalSystem)
    nodes = nodes.unique()
    neuron_groups = nodes.subset(NeuGroup)
    synapse_groups = nodes.subset(SynConn)
    ds_views = nodes.subset(DSView)
    other_nodes = nodes - neuron_groups - synapse_groups - ds_views

    # shared arguments

    # update synapse nodes
    for node in synapse_groups.values():
      node()

    # update neuron nodes
    for node in neuron_groups.values():
      node()

    # update other types of nodes
    for node in other_nodes.values():
      node()

    # update delays
    self.update_local_delays(nodes)

  def reset_state(self, batch_size=None):
    nodes = self.nodes(level=1, include_self=False).subset(DynamicalSystem).unique()
    neuron_groups = nodes.subset(NeuGroup)
    synapse_groups = nodes.subset(SynConn)

    # reset neuron nodes
    for node in neuron_groups.values():
      node.reset_state(batch_size)

    # reset synapse nodes
    for node in synapse_groups.values():
      node.reset_state(batch_size)

    # reset other types of nodes
    for node in (nodes - neuron_groups - synapse_groups).values():
      node.reset_state(batch_size)

    # reset delays
    self.reset_local_delays(nodes)


class System(Network):
  pass


class NeuGroup(DynamicalSystem):
  """Base class to model neuronal groups.

  There are several essential attributes:

  - ``size``: the geometry of the neuron group. For example, `(10, )` denotes a line of
    neurons, `(10, 10)` denotes a neuron group aligned in a 2D space, `(10, 15, 4)` denotes
    a 3-dimensional neuron group.
  - ``num``: the flattened number of neurons in the group. For example, `size=(10, )` => \
    `num=10`, `size=(10, 10)` => `num=100`, `size=(10, 15, 4)` => `num=600`.

  Parameters
  ----------
  size : int, tuple of int, list of int
    The neuron group geometry.
  name : optional, str
    The name of the dynamic system.
  keep_size: bool
    Whether keep the geometry information.

    .. versionadded:: 2.1.13
  mode: Mode
    The computing mode.

    .. versionadded:: 2.2.0
  """

  def __init__(
      self,
      size: Shape,
      keep_size: bool = False,
      name: str = None,
      mode: bm.Mode = None,
  ):
    # size
    if isinstance(size, (list, tuple)):
      if len(size) <= 0:
        raise ValueError(f'size must be int, or a tuple/list of int. '
                         f'But we got {type(size)}')
      if not isinstance(size[0], (int, np.integer)):
        raise ValueError('size must be int, or a tuple/list of int.'
                         f'But we got {type(size)}')
      size = tuple(size)
    elif isinstance(size, (int, np.integer)):
      size = (size,)
    else:
      raise ValueError('size must be int, or a tuple/list of int.'
                       f'But we got {type(size)}')
    self.size = size
    self.keep_size = keep_size

    # number of neurons
    self.num = tools.size2num(size)

    # initialize
    super(NeuGroup, self).__init__(name=name, mode=mode)

  @property
  def varshape(self):
    """The shape of variables in the neuron group."""
    return self.size if self.keep_size else (self.num,)

  def __repr__(self):
    return f'{self.__class__.__name__}(name={self.name}, mode={self.mode}, size={self.size})'

  def get_batch_shape(self, batch_size=None):
    if batch_size is None:
      return self.varshape
    else:
      return (batch_size,) + self.varshape

  def update(self, *args, **kwargs):
    """The function to specify the updating rule.
    """
    raise NotImplementedError(f'Subclass of {self.__class__.__name__} must '
                              f'implement "update" function.')

  def clear_input(self):
    """Function to clear inputs in the neuron group.
    It will be useful when monitoring inputs of the object received."""
    pass

  def __getitem__(self, item):
    return NeuGroupView(target=self, index=item)


class SynConn(DynamicalSystem):
  """Base class to model two-end synaptic connections.

  Parameters
  ----------
  pre : NeuGroup
    Pre-synaptic neuron group.
  post : NeuGroup
    Post-synaptic neuron group.
  conn : optional, ndarray, ArrayType, dict, TwoEndConnector
    The connection method between pre- and post-synaptic groups.
  name : str, optional
    The name of the dynamic system.
  """

  def __init__(
      self,
      pre: NeuGroup,
      post: NeuGroup,
      conn: Union[TwoEndConnector, ArrayType, Dict[str, ArrayType]] = None,
      name: str = None,
      mode: bm.Mode = None,
  ):
    super(SynConn, self).__init__(name=name, mode=mode)

    # pre or post neuron group
    # ------------------------
    if not isinstance(pre, (NeuGroup, DynamicalSystem)):
      raise TypeError('"pre" must be an instance of NeuGroup.')
    if not isinstance(post, (NeuGroup, DynamicalSystem)):
      raise TypeError('"post" must be an instance of NeuGroup.')
    self.pre = pre
    self.post = post

    # connectivity
    # ------------
    if isinstance(conn, TwoEndConnector):
      self.conn = conn(pre.size, post.size)
    elif isinstance(conn, (bm.ndarray, np.ndarray, jax.Array)):
      if (pre.num, post.num) != conn.shape:
        raise ValueError(f'"conn" is provided as a matrix, and it is expected '
                         f'to be an array with shape of (pre.num, post.num) = '
                         f'{(pre.num, post.num)}, however we got {conn.shape}')
      self.conn = MatConn(conn_mat=conn)
    elif isinstance(conn, dict):
      if not ('i' in conn and 'j' in conn):
        raise ValueError(f'"conn" is provided as a dict, and it is expected to '
                         f'be a dictionary with "i" and "j" specification, '
                         f'however we got {conn}')
      self.conn = IJConn(i=conn['i'], j=conn['j'])
    elif isinstance(conn, str):
      self.conn = conn
    elif conn is None:
      self.conn = None
    else:
      raise ValueError(f'Unknown "conn" type: {conn}')

  def __repr__(self):
    names = self.__class__.__name__
    return (f'{names}(name={self.name}, mode={self.mode}, \n'
            f'{" " * len(names)} pre={self.pre}, \n'
            f'{" " * len(names)} post={self.post})')

  def check_pre_attrs(self, *attrs):
    """Check whether pre group satisfies the requirement."""
    if not hasattr(self, 'pre'):
      raise ValueError('Please call __init__ function first.')
    for attr in attrs:
      if not isinstance(attr, str):
        raise TypeError(f'Must be string. But got {attr}.')
      if not hasattr(self.pre, attr):
        raise ValueError(f'{self} need "pre" neuron group has attribute "{attr}".')

  def check_post_attrs(self, *attrs):
    """Check whether post group satisfies the requirement."""
    if not hasattr(self, 'post'):
      raise ValueError('Please call __init__ function first.')
    for attr in attrs:
      if not isinstance(attr, str):
        raise TypeError(f'Must be string. But got {attr}.')
      if not hasattr(self.post, attr):
        raise ValueError(f'{self} need "pre" neuron group has attribute "{attr}".')

  def update(self, *args, **kwargs):
    """The function to specify the updating rule.

    Assume any dynamical system depends on the shared variables (`sha`),
    like time variable ``t``, the step precision ``dt``, and the time step `i`.
    """
    raise NotImplementedError('Must implement "update" function by subclass self.')


class _SynComponent(DynamicalSystem):
  """Base class for modeling synaptic components,
  including synaptic output, synaptic short-term plasticity,
  synaptic long-term plasticity, and others. """

  '''Master of this component.'''
  master: SynConn

  def __init__(self, *args, **kwargs):
    super(_SynComponent, self).__init__(*args, **kwargs)

    self._registered = False

  @property
  def isregistered(self) -> bool:
    """State of the component, representing whether it has been registered."""
    return self._registered

  @isregistered.setter
  def isregistered(self, val: bool):
    if not isinstance(val, bool):
      raise ValueError('Must be an instance of bool.')
    self._registered = val

  def reset_state(self, batch_size=None):
    pass

  def register_master(self, master: SynConn):
    if not isinstance(master, SynConn):
      raise TypeError(f'master must be instance of {SynConn.__name__}, but we got {type(master)}')
    if self.isregistered:
      raise ValueError(f'master has been registered, but we got another master going to be registered.')
    if hasattr(self, 'master') and self.master != master:
      raise ValueError(f'master has been registered, but we got another master going to be registered.')
    self.master = master
    self._registered = True

  def __repr__(self):
    return self.__class__.__name__

  def __call__(self, *args, **kwargs):
    return self.filter(*args, **kwargs)

  def clone(self) -> '_SynComponent':
    """The function useful to clone a new object when it has been used."""
    raise NotImplementedError

  def filter(self, g):
    raise NotImplementedError


class SynOut(_SynComponent):
  """Base class for synaptic current output."""

  def __init__(
      self,
      name: str = None,
      target_var: Union[str, Variable] = None,
  ):
    super(SynOut, self).__init__(name=name)
    # check target variable
    if target_var is not None:
      if not isinstance(target_var, (str, Variable)):
        raise TypeError('"target_var" must be instance of string or Variable. '
                        f'But we got {type(target_var)}')
    self.target_var: Optional[Variable] = target_var

  def register_master(self, master: SynConn):
    super(SynOut, self).register_master(master)

    # initialize target variable to output
    if isinstance(self.target_var, str):
      if not hasattr(self.master.post, self.target_var):
        raise KeyError(f'Post-synaptic group does not have target variable: {self.target_var}')
      self.target_var = getattr(self.master.post, self.target_var)

  def filter(self, g):
    if self.target_var is None:
      return g
    else:
      self.target_var += g

  def update(self, tdi):
    pass


class SynSTP(_SynComponent):
  """Base class for synaptic short-term plasticity."""

  def update(self, tdi, pre_spike):
    pass


class SynLTP(_SynComponent):
  """Base class for synaptic long-term plasticity."""

  def update(self, tdi, pre_spike):
    pass


class NullSynOut(SynOut):
  def clone(self):
    return NullSynOut()


class TwoEndConn(SynConn):
  """Base class to model synaptic connections.

  Parameters
  ----------
  pre : NeuGroup
    Pre-synaptic neuron group.
  post : NeuGroup
    Post-synaptic neuron group.
  conn : optional, ndarray, ArrayType, dict, TwoEndConnector
    The connection method between pre- and post-synaptic groups.
  output: Optional, SynOutput
    The output for the synaptic current.

    .. versionadded:: 2.1.13
       The output component for a two-end connection model.

  stp: Optional, SynSTP
    The short-term plasticity model for the synaptic variables.

    .. versionadded:: 2.1.13
       The short-term plasticity component for a two-end connection model.

  ltp: Optional, SynLTP
    The long-term plasticity model for the synaptic variables.

    .. versionadded:: 2.1.13
       The long-term plasticity component for a two-end connection model.

  name: Optional, str
    The name of the dynamic system.
  """

  def __init__(
      self,
      pre: NeuGroup,
      post: NeuGroup,
      conn: Union[TwoEndConnector, ArrayType, Dict[str, ArrayType]] = None,
      output: SynOut = NullSynOut(),
      stp: Optional[SynSTP] = None,
      ltp: Optional[SynLTP] = None,
      mode: bm.Mode = None,
      name: str = None,
  ):
    super(TwoEndConn, self).__init__(pre=pre,
                                     post=post,
                                     conn=conn,
                                     name=name,
                                     mode=mode)

    # synaptic output
    output = NullSynOut() if output is None else output
    if output.isregistered: output = output.clone()
    if not isinstance(output, SynOut):
      raise TypeError(f'output must be instance of {SynOut.__name__}, '
                      f'but we got {type(output)}')
    output.register_master(master=self)
    self.output: SynOut = output

    # short-term synaptic plasticity
    if stp is not None:
      if stp.isregistered: stp = stp.clone()
      if not isinstance(stp, SynSTP):
        raise TypeError(f'Short-term plasticity must be instance of {SynSTP.__name__}, '
                        f'but we got {type(stp)}')
      stp.register_master(master=self)
    self.stp: SynSTP = stp

    # long-term synaptic plasticity
    if ltp is not None:
      if ltp.isregistered: ltp = ltp.clone()
      if not isinstance(ltp, SynLTP):
        raise TypeError(f'Long-term plasticity must be instance of {SynLTP.__name__}, '
                        f'but we got {type(ltp)}')
      ltp.register_master(master=self)
    self.ltp: SynLTP = ltp

  def _init_weights(
      self,
      weight: Union[float, ArrayType, Initializer, Callable],
      comp_method: str,
      sparse_data: str = 'csr'
  ) -> Tuple[Union[float, ArrayType], ArrayType]:
    if comp_method not in ['sparse', 'dense']:
      raise ValueError(f'"comp_method" must be in "sparse" and "dense", but we got {comp_method}')
    if sparse_data not in ['csr', 'ij', 'coo']:
      raise ValueError(f'"sparse_data" must be in "csr" and "ij", but we got {sparse_data}')
    if self.conn is None:
      raise ValueError(f'Must provide "conn" when initialize the model {self.name}')

    # connections and weights
    if isinstance(self.conn, One2One):
      weight = parameter(weight, (self.pre.num,), allow_none=False)
      conn_mask = None

    elif isinstance(self.conn, All2All):
      weight = parameter(weight, (self.pre.num, self.post.num), allow_none=False)
      conn_mask = None

    else:
      if comp_method == 'sparse':
        if sparse_data == 'csr':
          conn_mask = self.conn.require('pre2post')
        elif sparse_data in ['ij', 'coo']:
          conn_mask = self.conn.require('post_ids', 'pre_ids')
        else:
          ValueError(f'Unknown sparse data type: {sparse_data}')
        weight = parameter(weight, conn_mask[0].shape, allow_none=False)
      elif comp_method == 'dense':
        weight = parameter(weight, (self.pre.num, self.post.num), allow_none=False)
        conn_mask = self.conn.require('conn_mat')
      else:
        raise ValueError(f'Unknown connection type: {comp_method}')

    # training weights
    if isinstance(self.mode, bm.TrainingMode):
      weight = bm.TrainVar(weight)
    return weight, conn_mask

  def _syn2post_with_all2all(self, syn_value, syn_weight):
    if bm.ndim(syn_weight) == 0:
      if isinstance(self.mode, bm.BatchingMode):
        post_vs = bm.sum(syn_value, keepdims=True, axis=tuple(range(syn_value.ndim))[1:])
      else:
        post_vs = bm.sum(syn_value)
      if not self.conn.include_self:
        post_vs = post_vs - syn_value
      post_vs = syn_weight * post_vs
    else:
      post_vs = syn_value @ syn_weight
    return post_vs

  def _syn2post_with_one2one(self, syn_value, syn_weight):
    return syn_value * syn_weight

  def _syn2post_with_dense(self, syn_value, syn_weight, conn_mat):
    if bm.ndim(syn_weight) == 0:
      post_vs = (syn_weight * syn_value) @ conn_mat
    else:
      post_vs = syn_value @ (syn_weight * conn_mat)
    return post_vs


class TwoEndConnNS(TwoEndConn):
  """Two-end connection without passing shared arguments."""
  _pass_shared_args = False


class CondNeuGroup(NeuGroup, Container):
  r"""Base class to model conductance-based neuron group.

  The standard formulation for a conductance-based model is given as

  .. math::

      C_m {dV \over dt} = \sum_jg_j(E - V) + I_{ext}

  where :math:`g_j=\bar{g}_{j} M^x N^y` is the channel conductance, :math:`E` is the
  reversal potential, :math:`M` is the activation variable, and :math:`N` is the
  inactivation variable.

  :math:`M` and :math:`N` have the dynamics of

  .. math::

      {dx \over dt} = \phi_x {x_\infty (V) - x \over \tau_x(V)}

  where :math:`x \in [M, N]`, :math:`\phi_x` is a temperature-dependent factor,
  :math:`x_\infty` is the steady state, and :math:`\tau_x` is the time constant.
  Equivalently, the above equation can be written as:

  .. math::

      \frac{d x}{d t}=\phi_{x}\left(\alpha_{x}(1-x)-\beta_{x} x\right)

  where :math:`\alpha_{x}` and :math:`\beta_{x}` are rate constants.

  .. versionadded:: 2.1.9
     Model the conductance-based neuron model.

  Parameters
  ----------
  size : int, sequence of int
    The network size of this neuron group.
  method: str
    The numerical integration method.
  name : optional, str
    The neuron group name.

  See Also
  --------
  Channel

  """

  def __init__(
      self,
      size: Shape,
      keep_size: bool = False,
      C: Union[float, ArrayType, Initializer, Callable] = 1.,
      A: Union[float, ArrayType, Initializer, Callable] = 1e-3,
      V_th: Union[float, ArrayType, Initializer, Callable] = 0.,
      V_initializer: Union[Initializer, Callable, ArrayType] = Uniform(-70, -60.),
      noise: Union[float, ArrayType, Initializer, Callable] = None,
      method: str = 'exp_auto',
      name: str = None,
      mode: bm.Mode = None,
      **channels
  ):
    NeuGroup.__init__(self, size, keep_size=keep_size, mode=mode)
    Container.__init__(self, **channels, name=name, mode=mode)

    # parameters for neurons
    self.C = C
    self.A = A
    self.V_th = V_th
    self.noise = init_noise(noise, self.varshape, num_vars=3)
    self._V_initializer = V_initializer

    # variables
    self.V = variable(V_initializer, self.mode, self.varshape)
    self.input = variable(bm.zeros, self.mode, self.varshape)
    self.spike = variable(lambda s: bm.zeros(s, dtype=bool), self.mode, self.varshape)

    # function
    if self.noise is None:
      self.integral = odeint(f=self.derivative, method=method)
    else:
      self.integral = sdeint(f=self.derivative, g=self.noise, method=method)

  def derivative(self, V, t):
    Iext = self.input.value * (1e-3 / self.A)
    channels = self.nodes(level=1, include_self=False).subset(Channel).unique()
    for ch in channels.values():
      Iext = Iext + ch.current(V)
    return Iext / self.C

  def reset_state(self, batch_size=None):
    self.V.value = variable(self._V_initializer, batch_size, self.varshape)
    self.spike.value = variable(lambda s: bm.zeros(s, dtype=bool), batch_size, self.varshape)
    self.input.value = variable(bm.zeros, batch_size, self.varshape)
    for channel in self.nodes(level=1, include_self=False).subset(Channel).unique().values():
      channel.reset_state(self.V.value, batch_size=batch_size)

  def update(self, tdi, *args, **kwargs):
    V = self.integral(self.V.value, tdi['t'], tdi['dt'])

    channels = self.nodes(level=1, include_self=False).subset(Channel).unique()
    # check whether the children channels have the correct parents.
    check_master(type(self), **channels)

    # update variables
    for node in channels.values():
      node.update(tdi, self.V.value)
    self.spike.value = bm.logical_and(V >= self.V_th, self.V < self.V_th)
    self.V.value = V

  def register_implicit_nodes(self, *channels, **named_channels):
    check_master(type(self), *channels, **named_channels)
    super(CondNeuGroup, self).register_implicit_nodes(*channels, **named_channels)

  def clear_input(self):
    """Useful for monitoring inputs. """
    self.input.value = bm.zeros_like(self.input.value)


class Channel(DynamicalSystem):
  """Abstract channel class."""

  master_type = CondNeuGroup

  def __init__(
      self,
      size: Union[int, Sequence[int]],
      name: str = None,
      keep_size: bool = False,
      mode: bm.Mode = None,
  ):
    super(Channel, self).__init__(name=name, mode=mode)
    # the geometry size
    self.size = tools.to_size(size)
    # the number of elements
    self.num = tools.size2num(self.size)
    # variable shape
    self.keep_size = keep_size

  @property
  def varshape(self):
    return self.size if self.keep_size else self.num

  def update(self, tdi, V):
    raise NotImplementedError('Must be implemented by the subclass.')

  def current(self, V):
    raise NotImplementedError('Must be implemented by the subclass.')

  def reset_state(self, V, batch_size=None):
    raise NotImplementedError('Must be implemented by the subclass.')


def _check(master, child):
  if not hasattr(child, 'master_type'):
    raise ValueError('Child class should define "master_type" to specify the type of the master. '
                     f'But we did not found it in {child}')
  if not issubclass(master, child.master_type):
    raise TypeError(f'Type does not match. {child} requires a master with type '
                    f'of {child.master_type}, but the master now is {master}.')


def check_master(master, *channels, **named_channels):
  for channel in channels:
    if isinstance(channel, Channel):
      _check(master, channel)
    elif isinstance(channel, (list, tuple)):
      for ch in channel:
        _check(master, ch)
    elif isinstance(channel, dict):
      for ch in channel.values():
        _check(master, ch)
    else:
      raise ValueError(f'Do not support {type(channel)}.')
  for channel in named_channels.values():
    if not isinstance(channel, Channel):
      raise ValueError(f'Do not support {type(channel)}. ')
    _check(master, channel)


class DSView(DynamicalSystem):
  """DSView, an object used to get a view of a dynamical system instance.

  It can get a subset view of variables in a dynamical system instance.
  For instance,

  >>> import brainpy as bp
  >>> hh = bp.neurons.HH(10)
  >>> DSView(hh, slice(5, 10, None))
  >>> # or, simply
  >>> hh[5:]
  """

  def __init__(
      self,
      target: DynamicalSystem,
      index: Union[slice, Sequence, ArrayType],
      varshape: Tuple[int, ...] = None,
      name: str = None,
      mode: bm.Mode = None
  ):
    # initialization
    DynamicalSystem.__init__(self, name=name, mode=mode)

    # check target
    if not isinstance(target, DynamicalSystem):
      raise TypeError(f'Should be instance of DynamicalSystem, but we got {type(target)}.')
    self.target = target  # the target object to slice

    # check slicing
    if isinstance(index, (int, slice)):
      index = (index,)
    self.index = index  # the slice

    # get all variables for slicing
    if not hasattr(self.target, SLICE_VARS):
      if varshape is None:
        if isinstance(target, NeuGroup):
          varshape = target.varshape
        else:
          raise UnsupportedError('Should provide varshape when the target does '
                                 f'not define its {SLICE_VARS}')
      all_vars = target.vars(level=1, include_self=True, method='relative')
      all_vars = {k: v for k, v in all_vars.items()}  # TODO
      # all_vars = {k: v for k, v in all_vars.items() if v.nobatch_shape == varshape}
    else:
      all_vars = {}
      for var_str in getattr(self.target, SLICE_VARS):
        v = eval(f'target.{var_str}')
        all_vars[var_str] = v

    # slice variables
    self.slice_vars = dict()
    for k, v in all_vars.items():
      if v.batch_axis is not None:
        index = ((self.index[:v.batch_axis] +
                  (slice(None, None, None),) +
                  self.index[v.batch_axis:])
                 if len(self.index) > v.batch_axis else
                 (self.index + tuple([slice(None, None, None)
                                      for _ in range(v.batch_axis - len(self.index) + 1)])))
      else:
        index = self.index
      self.slice_vars[k] = VariableView(v, index)

    # sub-nodes
    nodes = target.nodes(method='relative', level=1, include_self=False).subset(DynamicalSystem)
    for k, node in nodes.items():
      if isinstance(node, NeuGroup):
        node = NeuGroupView(node, self.index)
      else:
        node = DSView(node, self.index, varshape)
      setattr(self, k, node)

  def __repr__(self):
    return f'{self.__class__.__name__}(target={self.target}, index={self.index})'

  def __getattribute__(self, item):
    try:
      slice_vars = object.__getattribute__(self, 'slice_vars')
      if item in slice_vars:
        value = slice_vars[item]
        return value
      return object.__getattribute__(self, item)
    except AttributeError:
      return object.__getattribute__(self, item)

  def __setattr__(self, key, value):
    if hasattr(self, 'slice_vars'):
      slice_vars = super(DSView, self).__getattribute__('slice_vars')
      if key in slice_vars:
        v = slice_vars[key]
        v.value = value
        return
    super(DSView, self).__setattr__(key, value)

  def update(self, *args, **kwargs):
    raise NoImplementationError(f'DSView {self} cannot be updated. Please update its parent {self.target}')

  def reset_state(self, batch_size=None):
    pass


@tools.numba_jit
def _slice_to_num(slice_: slice, length: int):
  # start
  start = slice_.start
  if start is None:
    start = 0
  if start < 0:
    start = length + start
  start = max(start, 0)
  # stop
  stop = slice_.stop
  if stop is None:
    stop = length
  if stop < 0:
    stop = length + stop
  stop = min(stop, length)
  # step
  step = slice_.step
  if step is None:
    step = 1
  # number
  num = 0
  while start < stop:
    start += step
    num += 1
  return num


class NeuGroupView(DSView, NeuGroup):
  """A view for a neuron group instance."""

  def __init__(
      self,
      target: NeuGroup,
      index: Union[slice, Sequence, ArrayType],
      name: str = None,
      mode: bm.Mode = None
  ):
    DSView.__init__(self, target, index)

    # check slicing
    var_shapes = target.varshape
    if len(self.index) > len(var_shapes):
      raise ValueError(f"Length of the index should be less than "
                       f"that of the target's varshape. But we "
                       f"got {len(self.index)} > {len(var_shapes)}")

    # get size
    size = []
    for i, idx in enumerate(self.index):
      if isinstance(idx, int):
        size.append(1)
      elif isinstance(idx, slice):
        size.append(_slice_to_num(idx, var_shapes[i]))
      else:
        # should be a list/tuple/array of int
        # do not check again
        if not isinstance(idx, collections.Iterable):
          raise TypeError('Should be an iterable object of int.')
        size.append(len(idx))
    size += list(var_shapes[len(self.index):])

    # initialization
    NeuGroup.__init__(self, tuple(size), name=name, mode=mode)


class DynamicalSystemNS(DynamicalSystem):
  """Dynamical system without the need to pass shared parameters into ``update()`` function."""

  _pass_shared_args = False


class Sequential(DynamicalSystemNS):
  """A sequential `input-output` module.

  Modules will be added to it in the order they are passed in the
  constructor. Alternatively, an ``dict`` of modules can be
  passed in. The ``update()`` method of ``Sequential`` accepts any
  input and forwards it to the first module it contains. It then
  "chains" outputs to inputs sequentially for each subsequent module,
  finally returning the output of the last module.

  The value a ``Sequential`` provides over manually calling a sequence
  of modules is that it allows treating the whole container as a
  single module, such that performing a transformation on the
  ``Sequential`` applies to each of the modules it stores (which are
  each a registered submodule of the ``Sequential``).

  What's the difference between a ``Sequential`` and a
  :py:class:`Container`? A ``Container`` is exactly what it
  sounds like--a container to store :py:class:`DynamicalSystem` s!
  On the other hand, the layers in a ``Sequential`` are connected
  in a cascading way.

  Examples
  --------

  >>> import brainpy as bp
  >>> import brainpy.math as bm
  >>>
  >>> # composing ANN models
  >>> l = bp.Sequential(bp.layers.Dense(100, 10),
  >>>                   bm.relu,
  >>>                   bp.layers.Dense(10, 2))
  >>> l({}, bm.random.random((256, 100)))
  >>>
  >>> # Using Sequential with Dict. This is functionally the
  >>> # same as the above code
  >>> l = bp.Sequential(l1=bp.layers.Dense(100, 10),
  >>>                   l2=bm.relu,
  >>>                   l3=bp.layers.Dense(10, 2))
  >>> l({}, bm.random.random((256, 100)))

  Parameters
  ----------
  name: str
    The object name.
  mode: Mode
    The object computing context/mode. Default is ``None``.
  """

  def __init__(
      self,
      *modules_as_tuple,
      name: str = None,
      mode: bm.Mode = None,
      **modules_as_dict
  ):
    super().__init__(name=name, mode=mode)
    self._dyn_modules = bm.NodeDict()
    self._static_modules = dict()
    i = 0
    for m in modules_as_tuple + tuple(modules_as_dict.values()):
      key = self.__format_key(i)
      if isinstance(m, bm.BrainPyObject):
        self._dyn_modules[key] = m
      else:
        self._static_modules[key] = m
      i += 1
    self._num = i

  def __format_key(self, i):
    return f'l-{i}'

  def __all_nodes(self):
    nodes = []
    for i in range(self._num):
      key = self.__format_key(i)
      if key not in self._dyn_modules:
        nodes.append(self._static_modules[key])
      else:
        nodes.append(self._dyn_modules[key])
    return nodes

  def __getitem__(self, key: Union[int, slice, str]):
    if isinstance(key, str):
      if key in self._dyn_modules:
        return self._dyn_modules[key]
      elif key in self._static_modules:
        return self._static_modules[key]
      else:
        raise KeyError(f'Does not find a component named {key} in\n {str(self)}')
    elif isinstance(key, slice):
      return Sequential(*(self.__all_nodes()[key]))
    elif isinstance(key, int):
      return self.__all_nodes()[key]
    elif isinstance(key, (tuple, list)):
      _all_nodes = self.__all_nodes()
      return Sequential(*[_all_nodes[k] for k in key])
    else:
      raise KeyError(f'Unknown type of key: {type(key)}')

  def __repr__(self):
    nodes = self.__all_nodes()
    entries = '\n'.join(f'  [{i}] {tools.repr_object(x)}' for i, x in enumerate(nodes))
    return f'{self.__class__.__name__}(\n{entries}\n)'

  def update(self, x):
    """Update function of a sequential model.
    """
    for m in self.__all_nodes():
      x = m(x)
    return x


class NeuGroupNS(NeuGroup):
  """Base class for neuron group without shared arguments passed."""
  _pass_shared_args = False

