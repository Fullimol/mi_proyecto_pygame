def punto_en_rectangulo(punto, rect)->bool:
    x, y = punto
    return x >= rect.left and x <= rect.right and y >= rect.top and y <= rect.bottom

def detectar_colision(rect_1, rect_2)->bool:
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