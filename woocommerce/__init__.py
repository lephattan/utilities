from typing import Dict, Optional, Union


class UnsupportedBulkEditAction(Exception):
    def __init__(self, msg: str = 'Unsupported bulk edit action', *args, action: Optional[str] = None, **kwargs ) -> None:
        if action is not None:
            msg = f"{msg}: {action}"
        super().__init__(msg, *args, **kwargs)


def bulk_edit(product_json: dict, edits: list) -> dict:
    """
    TODO: docs string
    """
    for edit in edits:
        if edit['target'] == 'variation':
            product_json = bulk_edit_variation(
                product_json, edit['field'], edit['action'], edit['value'])
        elif edit['target'] == 'product':
            product_json = bulk_edit_product(
                product_json, edit['field'], edit['action'], edit['value'])

    return product_json


def bulk_edit_variation(product_json: dict, field: str, action: str, value: Union[str, int, float]) -> Dict:
    """
    Modifies woocommerce product_json variations field with provied action and value
        Parameters:
            product_json (dict): woocommerce product json
            field (str): field to look for
            action (str): action to perform
            value (str|int|float): value to perform
        Returns:
            product_json (dict): woocommerce product json after edited
    """
    supported_actions = ['increase', 'decrease', 'append', 'prepend', 'remove']
    if action not in supported_actions:
        raise UnsupportedBulkEditAction('Unsupported bulk edit action: {}. Only accept: {}'.format(
            action, ' ,'.join(supported_actions)
            ))

    if product_json.get('variations'):
        for variation in product_json['variations']:
            if variation.get(field):
                if action == 'increase':
                    variation[field] = str(float(variation[field]) + float(value))
                elif action == 'decrease':
                    variation[field] = str(float(variation[field]) - float(value))
                elif action == 'append':
                    variation[field] = str(variation[field]) + str(value)
                elif action == 'prepend':
                    variation[field] = str(value) + str(variation[field])
                elif action == 'remove':
                    variation[field] = str(
                        variation[field]).replace(str(value), '')

    return product_json

def bulk_edit_product(product_json: dict, field: str, action: str, value: Union[str, int, float] ) -> Dict:
    if product_json.get(field):
        if action == 'increase':
            product_json[field] = str(float(product_json[field]) + float(value))
        elif action == 'decrease':
            product_json[field] = str(float(product_json[field]) - float(value))
        elif action == 'append':
            product_json[field] = str(product_json[field]) + str(value)
        elif action == 'prepend':
            product_json[field] = str(value) + str(product_json[field])
        elif action == 'remove':
            product_json[field] = str(
                product_json[field]).replace(str(value), '')

    return product_json
