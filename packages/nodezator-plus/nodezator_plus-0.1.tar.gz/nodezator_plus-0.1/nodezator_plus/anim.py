# from ..videopreview.cache import render_video_data

import cv2, pygame
from pathlib import Path

def nodezator_plus_animation():
    cap = cv2.VideoCapture(str(Path(__file__).parent)+"\\anim.mp4")
    success, img = cap.read()
    shape = img.shape[1::-1]
    wn = pygame.display.set_mode(shape)
    clock = pygame.time.Clock()
    while success:
        success, img = cap.read()
        if type(img)==type(None): return
        wn.blit(pygame.image.frombuffer(img.tobytes(), shape, "BGR"), (0,0))
        pygame.display.update()




nodezator_plus_animation()