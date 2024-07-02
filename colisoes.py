#Joao Vitor Bortoletto

import pygame  # Importa a biblioteca pygame para criar gráficos e interações
import random  # Importa a biblioteca random para gerar valores aleatórios
import numpy as np  # Importa a biblioteca numpy para cálculos matemáticos
import pygame.gfxdraw  # Importa o módulo gfxdraw do pygame para desenhar gráficos avançados

# Classe que representa a janela das partículas
class Ambiente():
    def __init__(self, DIM, dt):
        self.DIM = DIM  
        self.dt = dt    
        self.particulas = []  
        self.e = 0.8    # Coeficiente de restituição para colisões elásticas

    # Atualiza o estado do ambiente e das partículas
    def atualizar(self):
        for p1 in self.particulas:  # Para cada partícula no ambiente
            p1.atualizarEstado()  
            self.quicar(p1)  # Verifica colisões com as bordas da tela
            for p2 in self.particulas:  # Verifica colisões com outras partículas
                if p1 != p2:
                    self.colisaoElastica(p1, p2)  # Verifica e resolve colisões elásticas

    # Adiciona uma partícula ao ambiente
    def adicionarParticula(self, p):
        self.particulas.append(p)  

    # Verifica colisões com as bordas da tela e inverte a velocidade
    def quicar(self, p):
        for i in range(2):  # Para cada dimensão (x e y)
            if p.X[0][i] <= p.raio or p.X[0][i] >= self.DIM[i] - p.raio:
                p.V[0][i] *= -1  # Inverte a velocidade na direção da colisão

    # Verifica e trata colisões elásticas entre duas partículas
    def colisaoElastica(self, p1, p2):
        dX = p1.X - p2.X  # Vetor de distância entre as partículas
        dist = np.sqrt(np.sum(dX ** 2))  # Distância euclidiana entre as partículas
        
        if dist < p1.raio + p2.raio:  # Verifica se houve colisão
            n = dX / dist  
            v_rel = p1.V - p2.V  
            v_rel_dot_n = np.dot(v_rel, n.T)  # Projeção da velocidade relativa no vetor normal
            
            if v_rel_dot_n < 0:  # Se as partículas estão se aproximando
                e = self.e  # Coeficiente de restituição
                J = -(1 + e) * v_rel_dot_n / (1 / p1.massa + 1 / p2.massa) * n  # Impulso de colisão
                p1.adicionarVelocidade(J / p1.massa)  # Atualiza a velocidade da primeira partícula
                p2.adicionarVelocidade(-J / p2.massa)  # Atualiza a velocidade da segunda partícula
                
                # Corrige sobreposição das partículas após a colisão
                overlap = p1.raio + p2.raio - dist
                correction = (overlap / (p1.massa + p2.massa)) * n
                p1.adicionarPosicao(correction * p2.massa)
                p2.adicionarPosicao(-correction * p1.massa)

                # Calcula os ângulos de saída
                angulo_p1 = np.arctan2(p1.V[0][1], p1.V[0][0])
                angulo_p2 = np.arctan2(p2.V[0][1], p2.V[0][0])
                # Ângulos calculados mas não utilizados aqui

# Classe que representa uma partícula
class Particula():
    def __init__(self, ambiente, X, V, raio, massa):
        self.ambiente = ambiente  # Referência ao ambiente em que a partícula está
        self.X = X  # Posição da partícula 
        self.V = V  # Velocidade da partícula
        self.raio = raio  # Raio da partícula
        self.massa = massa  # Massa da partícula
        self.cor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # Cor da partícula (aleatória)

    # Adiciona velocidade à partícula
    def adicionarVelocidade(self, vel):
        self.V += vel  # Atualiza a velocidade da partícula
    
    # Adiciona posição à partícula
    def adicionarPosicao(self, pos):
        self.X += pos  # Atualiza a posição da partícula

    # Atualiza o estado da partícula com base na velocidade e no tempo
    def atualizarEstado(self): 
        self.X += self.V * self.ambiente.dt  # Atualiza posição com base na velocidade e no intervalo de tempo

# Função principal que configura e executa a simulação
def main():
    DIM = np.array ([700, 700]) # Dimensões da tela
    dt = 0.01  # Intervalo de tempo para atualização (60 fps)
    ambiente = Ambiente(DIM,  dt)  # Cria o ambiente de simulação

    pygame.init()  
    tela = pygame.display.set_mode((DIM[0], DIM[1]))  # Cria a tela de exibição
    pygame.display.set_caption('Projeto de colisoes elasticas, Fisica Teorica 1')

    numero_de_particulas = int(input("Digite o número de partículas: "))  

    # Cria partículas com parâmetros aleatórios
    for n in range(numero_de_particulas):
        raio = np.random.randint(10, 20)  
        massa = np.random.uniform(1, 10)  
        X = np.random.rand(1, 2) * (DIM - raio * 2) + raio  
        V = np.random.uniform(-50, 50, (1, 2))  
        particula = Particula(ambiente, X, V, raio, massa)  
        ambiente.adicionarParticula(particula)  # Adiciona a partícula ao ambiente

    # Função para desenhar as partículas na tela
    def exibir(ambiente):
        for p in ambiente.particulas:
            pygame.gfxdraw.filled_circle(tela, int(p.X[0][0]), int(p.X[0][1]), p.raio, p.cor)  # Desenha cada partícula na tela

    executando = True
    while executando:
        for evento in pygame.event.get():  # Captura eventos do pygame
            if evento.type == pygame.QUIT:  # Se o evento for fechar a janela
                executando = False  # Encerra o loop principal
        tela.fill([0, 0, 0])  # Limpa a tela com cor preta
        ambiente.atualizar()  # Atualiza o ambiente e as partículas
        exibir(ambiente)  # Desenha as partículas na tela
        pygame.display.flip()  # Atualiza a tela

    pygame.quit()  # Finaliza o pygame ao sair do loop principal

if __name__ == "__main__":
    main()  # Executa a função principal se este arquivo for o script principal



