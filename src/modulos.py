import pygame
from settings import WHITE
import sys

# configuro la fuente del texto
def mostrar_texto(superficie:pygame.Surface, coordenada:tuple[int, int], texto:str, fuente:pygame.font.Font, color:tuple[int, int, int]= WHITE, background_color:tuple[int, int, int]= None ):
    """ Renderiza un texto en una superficie

    Args:
        superficie (pygame.Surface): Surface donde se renderiza.
        coordenada (tuple[int, int]): ubicación en la pantalla.
        texto (str): texto a mostrar.
        fuente (pygame.font.Font): estilo de la fuente.
        color (tuple[int, int, int], optional): color de texto.
        background_color (tuple[int, int, int], optional): color de fondo.
    """
    sup_texto = fuente.render(texto , True, color, background_color)
    rect_texto = sup_texto.get_rect()
    rect_texto.center = coordenada
    superficie.blit(sup_texto, rect_texto)


# Cargar imagenes
def escalar_imagenes(imagen:str, width:int, height:int) -> pygame.Surface:
    """ Recibe la URL de la imagen y la escala.

    Args:
        imagen (str): URL de la imagen.
        width (int): Ancho de la imagen.
        height (int): Alto de la imagen.

    Returns:
        _type_: la surface de la imagen escalada.
    """
    try:
        imagen_surface =pygame.image.load(imagen)
    except:
        print("Error al cargar la imagen")
    return pygame.transform.scale(imagen_surface, (width, height))


def cargar_sonido(sonido:str, volumen:float) -> pygame.mixer.Sound:
    """ Recibe un sonido y lo carga con el volumen establecido.

    Args:
        sonido (str): URL del sonido.
        volumen (float): Volumen del sonido.

    Returns:
        pygame.mixer.Sound: el sonido cargado.
    """
    try:
        sonido_cargado = pygame.mixer.Sound(sonido)
        sonido_cargado.set_volume(volumen)
    except:
        print("Error al cargar el sonido o indicar volumen")
    return sonido_cargado
    

def terminar():
    pygame.quit()
    sys.exit()


def wait_user(tecla:int, sonido_tecla:pygame.mixer.Sound) -> None:
    """ Espera que el usuario presione una tecla.

    Args:
        tecla (int): pasamos la tecla a presionar. (Pygame lo pasa como codigo ASCII).
        sonido_tecla (pygame.mixer.Sound): efecto sonido al presionar tecla.
    """
    flag_start = True
    while flag_start:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                terminar()
            if evento.type == pygame.KEYDOWN:
                if evento.key == tecla:
                    sonido_tecla.play()
                    flag_start = False

# guardar el score en un archivo .csv
def save_data(data) -> None:
    """ Guardar dato en un archivo .csv.

    Args:
        data (any): dato a guardar.
    """
    try:
        with open("score.csv", "a") as archivo:
            archivo.write(f"{data}\n")
    except:
        print("Error al intentar guardar el .CSV")

    

#funcion leer Json
def load_json(url:str) -> dict:
    """ lee un archivo json.

    Args:
        url (str): url del archivo.

    Returns:
        dict: el json en un diccionario.
    """
    import json
    try:
        with open(url, "r") as archivo:
            return json.load(archivo)
    except:
        print("Error al intentar leer el .JSON")