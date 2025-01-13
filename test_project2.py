from project2 import ISPNetwork
import random

if __name__ == '__main__':
    print("--------- Task1 build graph ---------")
    # Note: You should try all six dataset. This is just a example using 1221.csv
    net = ISPNetwork()
    net.buildGraph('data/1221.csv')

    print("--------- Task2 check if path exists ---------")
    routers = [v.id for v in random.sample(list(net.network.vertList.values()), 5)]
    for i in range(4):
        print('Router1:', routers[i], ', Router2:', routers[i + 1], 'path exist within 5 hops?:',
              net.pathExist(routers[i], routers[i + 1], 5))

    print("--------- Task3 build MST ---------")
    net.buildMST(routers[0])
    print('graph node size', net.MST.numVertices)

    print("--------- Task4 find shortest path in MST ---------")
    for i in range(4):
        print(routers[i], routers[i + 1], 'Path:', net.findPath(routers[i], routers[i + 1]))

    print("--------- Task5 find shortest path in original graph ---------")
    for i in range(4):
        print(routers[i], routers[i + 1], 'Path:', net.findForwardingPath(routers[i], routers[i + 1]))

    print("--------- Task6 find path in LowestMaxWeightFirst algorithm ---------")
    for i in range(4):
        print(routers[i], routers[i + 1], 'Path:', net.findPathMaxWeight(routers[i], routers[i + 1]))

    print("--------- Task7 identify loop ---------")

    route = {
        "MelbourneAustralia3870": "MelbourneAustralia3882",
        "MelbourneAustralia3882": "MelbourneAustralia734",
        "MelbourneAustralia734": "MelbourneAustralia3881",
        "MelbourneAustralia3881": "MelbourneAustralia3870"
    }  # This one is a loop
    print(net.checkLoop(route))

    route = {
        "RockhamptonAustralia4195": "BrisbaneAustralia1769",
        "BrisbaneAustralia1769": "TownsvilleAustralia4282"
    } # This one is NOT a loop
    print(net.checkLoop(route))
