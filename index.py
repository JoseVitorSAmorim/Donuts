import math
import os
import time

def main():
    # Ângulos de rotação iniciais
    A = 0
    B = 0
    
    # Configurações do "render"
    # Caracteres de brilho (do mais escuro para o mais claro)
    chars = ".,-~:;=!*#$@"
    
    print("\033[2J") # Limpa a tela uma vez

    while True:
        z = [0] * 1760    # Buffer de profundidade (z-buffer)
        b = [' '] * 1760  # Buffer de caracteres (tela)
        
        # Loop para desenhar o círculo interno (theta)
        j = 0
        while j < 6.28:
            j += 0.07
            # Loop para rotacionar o círculo e formar o toro (phi)
            i = 0
            while i < 6.28:
                i += 0.02

                sin_i = math.sin(i)
                cos_j = math.cos(j)
                sin_A = math.sin(A)
                sin_j = math.sin(j)
                cos_A = math.cos(A)
                cos_i = math.cos(i)
                cos_B = math.cos(B)
                sin_B = math.sin(B)
                
                h = cos_j + 2 # R1 + R2 * cos(theta)
                D = 1 / (sin_i * h * sin_A + sin_j * cos_A + 5) # Projeção 1/z
                t = sin_i * h * cos_A - sin_j * sin_A

                # Coordenadas projetadas na tela (x, y)
                x = int(40 + 30 * D * (cos_i * h * cos_B - t * sin_B))
                y = int(12 + 15 * D * (cos_i * h * sin_B + t * cos_B))
                
                # Índice no array linear da tela
                o = int(x + 80 * y)
                
                # Cálculo da luminosidade (brilho)
                N = int(8 * ((sin_j * sin_A - sin_i * cos_j * cos_A) * cos_B - sin_i * cos_j * sin_A - sin_j * cos_A - cos_i * cos_j * sin_B))

                # Verifica se o ponto está dentro da tela e se é o mais próximo (z-buffer)
                if 0 <= y < 22 and 0 <= x < 80 and D > z[o]:
                    z[o] = D
                    b[o] = chars[N if N > 0 else 0]

        # Move o cursor para o topo da tela em vez de limpar tudo (evita flicker)
        print("\033[H", end="")
        
        # Exibe o buffer na tela
        for k in range(1761):
            print(b[k] if k % 80 else '\n', end="")
        
        # Incrementa os ângulos para a próxima rotação
        A += 0.04
        B += 0.02
        
        # Pequena pausa para controlar a velocidade
        time.sleep(0.01)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAnimação encerrada.")
