from random import choice, shuffle, random
from collections import deque
import time
   # 5 minutes from now


# Creates Genome
def genome_random(length_genome, bases, repeat_str, z):
    genome = ""
    count = 0
    
    z_count =  int(length_genome/z - z)

    while(length_genome > 0):
        if(count == z_count):
            genome += repeat_str
            length_genome -= len(repeat_str)
            count = 0
            continue
        else:   
            inp = choice(bases)
            genome += inp
            length_genome -= len(inp)
            count = count + 1
    
    return genome

# Repeat Creator if Repeats are allowed
def repeat_creator(length, y, z):
    repeat = genome_random(y, ['A','C','T','G'], "", -1) #creates random string, 5
    print("This is the repeat: " +  repeat + "\n\n")
    return genome_random(length, ['A', 'C', 'T', 'G'], repeat, z)


# Creates list of k-mers
def k_mer(h_gene, x):
    k_mers = []
    for i in range(len(h_gene)):
        for j in range(i + 1, len(h_gene) + 1):
            if(len(h_gene[i:j]) == x):
                k_mers.append(h_gene[i:j])
    
    return k_mers

# Construct De Bruijn Graph
def construct(input):
    edges = input
    graph = {}
    
    for edge in edges:
        frm = edge[:len(edge)-1]
        to = edge[1:]
        if frm in graph:
            graph[frm].append(to)
        else:
            graph[frm]=[to]

    
    for val in graph.values():
        val.sort()

    
    # for k ,v in (graph.items()):
    #     print(k+' -> '+','.join(v))

    return (graph)

# Construct Genome from De Bruijn Graph
def reconstruct(graph, firstNode, lastNode):
    #add edge from last node to first node
    frm = lastNode[1:]
    to = firstNode[:len(firstNode) - 1]
    if frm in graph:
        graph[frm].append(to)
    else:
        graph[frm]=[to]
   
    #find euler cycle
    cur = to
    cycle = deque()
    num_edges = sum(map(len, graph.values())) #6
    while(num_edges > 0):
        choices = graph[cur]

        while choices:
            cycle.append(cur) #c = [CT, GT]
            num_edges -= 1
            cur = choices.pop() #cur = CT
            choices = graph.get(cur, None) #choices = AC
        
        if num_edges == 0:
            break
    
        rotate = 0
        for cur in cycle: 
            if graph[cur]:
                break
            rotate += 1

        cycle.rotate(-rotate)

    cycle.rotate(-cycle.index(to))


    return string_convert(list(cycle))

# Conver Genome List to String
def string_convert(cycle):
    gene_str = cycle[0]
    for i in range(1, len(cycle)):
        gene_str += cycle[i][-1]
    return gene_str


# Main Calling Function
def runner(x, y, z, repeat):
    if(not repeat):
        genome = genome_random(1000, ['A','C','T','G'], "", -1)
    else:
        genome = repeat_creator(1000, y, z)
    print("Genome: " + genome + "\n\n")
    k_list = k_mer(genome, x)
    count = 0
    timeout = time.time() + 60*1
    orig_genome = ""
    while(genome != orig_genome):  
        if(time.time() > timeout):
            print("TIMEOUT 1 MINUTE")
            break
        graph = construct(k_list)
        for i in graph.values():
            shuffle(i)
        orig_genome = (reconstruct(graph, k_list[0], k_list[-1]))
        count += 1
        print("Reconstruct Genome: " + orig_genome + "\n\n")

    print("Number of Random Walks: " + str(count))
    if(genome == orig_genome):
        print("WAHOOOOOOOOOO")
    else:
        print("rip :(")


def main():
    runner(23, 20, 10, True)


if __name__ == "__main__":
    main()

