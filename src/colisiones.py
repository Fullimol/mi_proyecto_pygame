def punto_en_rectangulo(punto:tuple, rect:tuple)->bool:
    """ Revisa si un punto se encuentra dentro de un rectangulo.

    Args:
        punto (tuple): coordenadas del punto.
        rect (tuple): coordenadas del rectangulo.

    Returns:
        bool: True si el punto se encuentra dentro del rectangulo.
    """
    x, y = punto
    return x >= rect.left and x <= rect.right and y >= rect.top and y <= rect.bottom

def detectar_colision(rect_1:tuple, rect_2:tuple)->bool:
    """ Revisa si dos rectangulos se intersectan.

    Args:
        rect_1 (tuple): pasamos el rectangulo 1.
        rect_2 (tuple): pasamos el rectangulo 2.

    Returns:
        bool: comprueba cada vertice del rectangulo 1 y el rectangulo 2.
              si se tocan, devuelve True.
    """
    # Revisa si algún punto de rec_1 esta dentro de rec_2
    if punto_en_rectangulo(rect_1.topleft, rect_2) or \
       punto_en_rectangulo(rect_1.topright, rect_2) or\
       punto_en_rectangulo(rect_1.bottomleft, rect_2) or\
       punto_en_rectangulo(rect_1.bottomright, rect_2):
        return True
    
    # Revisa si qué punto de rec_2 esta dentro de rec_1
    if punto_en_rectangulo(rect_2.topleft, rect_1) or \
       punto_en_rectangulo(rect_2.topright, rect_1) or\
       punto_en_rectangulo(rect_2.bottomleft, rect_1) or\
       punto_en_rectangulo(rect_2.bottomright, rect_1):
        return True