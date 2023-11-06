def correct_values(var, offset=30, scale_factor=0.001):
    """
    Funcion que corrige el offset y scale factor en caso de ser necesario.
    """
    return (var - offset)/scale_factor