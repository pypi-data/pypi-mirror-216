from ..classes.cell import CellTemplate
from ..classes.agent import AgentTemplate
from types import ModuleType


def class_from_rule(targetClass, rule):
    # {{{
    if rule in targetClass.__subclasses__():
        return rule
    elif isinstance(rule, ModuleType):
        relevant_items = [name for name in dir(rule) if name[:2] != "__"]

        for name in relevant_items:
            rule_dict_entry = rule.__dict__[name]
            if rule_dict_entry in targetClass.__subclasses__():
                return rule_dict_entry

        raise TypeError(
            f"Module '{rule.__name__}' does not contain a Cell or "
            "Agent class."
        )

    else:
        raise TypeError(
            f"Type {type(rule)} is invalid for the 'rule' parameter. "
            "Valid types are CellTemplate, ModuleType and AgentTemplate."
        )


# }}}


def cell_from_rule(rule):
    # {{{
    """
    A regra pode ser um módulo de Python contendo uma classe que herda de
    CellTemplate, ou a própria classe. Esta função existe para que as
    demais funções deste módulo se adequem a estes requisitos.
    """

    return class_from_rule(CellTemplate, rule)


# }}}


def agent_from_rule(rule):
    # {{{
    """
    A regra pode ser um módulo de Python contendo uma classe que herda de
    CellTemplate, ou a própria classe. Esta função existe para que as demais
    funções deste módulo se adequem a estes requisitos.
    """

    return class_from_rule(AgentTemplate, rule)


# }}}
