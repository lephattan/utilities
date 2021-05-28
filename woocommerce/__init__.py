class UnsupportedBulkEditAction(Exception):
    pass


def bulk_edit_variation(product_json: dict, field: str, action: str, value: str or int or float) -> dict:
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
                    variation[field] = float(variation[field]) + float(value)
                elif action == 'decrease':
                    variation[field] = float(variation[field]) - float(value)
                elif action == 'append':
                    variation[field] = str(variation[field]) + str(value)
                elif action == 'prepend':
                    variation[field] = str(value) + str(variation[field])
                elif action == 'remove':
                    variation[field] = str(
                        variation[field]).replace(str(value), '')

    return product_json
