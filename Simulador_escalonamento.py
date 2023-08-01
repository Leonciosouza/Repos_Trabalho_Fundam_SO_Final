# Desenvolva um simulador de escalonamento de processos para um sistema operacional. O referido simulador devel combinar o algoritmo de alocação dinâmica Best-Fit
# para gerenciar a memória e o escalonamento Round Robin para a CPU. O Sistema Operacional  possui uma lista de processos a serem executados, cada um com o seu tamanho de memória necessário e tempo de execução(...).


import heapq


class Process:
    def __init__(self, name, memory_size, execution_time):
        self.name = name
        self.memory_size = memory_size
        self.execution_time = execution_time
        self.remaining_time = execution_time
        self.memory_block = None  # O bloco de memória atribuído a este processo!

    def __lt__(self, other):
        # Usado para comparar processos na fila de prontos (heap)!
        return self.remaining_time < other.remaining_time


def best_fit(memory_blocks, process):
    # Encontre o bloco de memória mais adequado para alocar o processo!
    best_block = None
    for block in memory_blocks:
        if block[0] >= process.memory_size:
            if best_block is None or block[0] < best_block[0]:
                best_block = block
                
    if best_block is not None:
        block_size, block_start = best_block
        
        if block_size > process.memory_size:
            memory_blocks.insert(block_start, (block_size - process.memory_size, block_start + process.memory_size))
        return block_start
    del memory_blocks[block_start]
    return -1


def agendador_processos(processos_Corrente, memory_size, quantumm):
    memory_blocks = [(memory_size, 0)]  # Inicialmente, temos um único bloco de memória!
    ready_queue = []  # Fila de prontos usando um heap para escalonamento Round Robin!
    result = []
    current_time = 1
    while processos_Corrente or ready_queue:
        # Adiciona processos à fila de prontos que chegaram no momento atual
        while processos_Corrente and processos_Corrente[0].execution_time <= current_time:
            process = processos_Corrente.pop(0)
            process.memory_block = best_fit(memory_blocks, process)
            if process.memory_block != -1:
                heapq.heappush(ready_queue, process)

        if ready_queue:
            current_process = heapq.heappop(ready_queue)
            remaining_time = min(quantumm, current_process.remaining_time)
            current_process.remaining_time -= remaining_time
            current_time += remaining_time
            result.append((current_time, current_process.name))

            # Libera memória do processo que terminou a execução!
            if current_process.remaining_time == 0:
                memory_blocks.insert(current_process.memory_block,
                                     (current_process.memory_size, current_process.memory_block))
        
        current_time = current_time + 1

    return result


# Script de teste:
if __name__ == "__main__":
    print("teste")
    processosCorrente = [
        Process("P1", 2, 2),
        Process("P2", 4, 4),
        Process("P3", 1, 5),
        Process("P4", 3, 3),
        Process("P5", 4, 7)
    ]

    memory_size = 10
    quantum = 2

    ordem_execucao = agendador_processos(processosCorrente, memory_size, quantum)

    for t, process_name in ordem_execucao:
        print(f"Tempo: {t} - Executando processo: {process_name}")
