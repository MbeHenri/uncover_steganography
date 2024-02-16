from sklearn.cluster import KMeans

from src.utils.functions import regroup_datas


class NodeBow:
    def __init__(self, kmeans: KMeans = None) -> None:
        self.kmeans = kmeans
        self.childreen = None
        self.patchs = None

    def addChildreen(self, label_node, node):
        if self.childreen is None:
            self.childreen = {}
        self.childreen[label_node] = node

    def setPatchs(self, patch_datas: list):
        self.kmeans = None
        self.childreen = None
        self.patchs = patch_datas

    def getDuplicatePatchs(self, features_patch: list):
        if self.kmeans is None:
            return self.patchs
        else:
            try:
                child = self.childreen[
                    self.kmeans.predict([features_patch]).tolist()[0]
                ]
                return child.getDuplicatePatchs(features_patch)
            except KeyError:
                return None


class TreeBow:
    def __init__(self, racine: NodeBow):
        self.racine = racine

    def getDuplicatePatchs(self, features_patch):
        return self.racine.getDuplicatePatchs(features_patch)


def hierarchicalBOW(datas: list, depth=3, K=2):
    node = NodeBow()
    n = len(datas)
    if depth > 0 and n > K:
        kmeans = KMeans(n_clusters=K, n_init="auto")
        kmeans.fit(
            [datas[i]["data"] for i in range(n)],
        )
        node.kmeans = kmeans

        next_datas = regroup_datas(datas, kmeans.labels_.tolist())
        for label, data in next_datas.items():
            node_child = hierarchicalBOW(data, depth=depth - 1, K=K)
            node.addChildreen(label, node_child)

    else:
        node.setPatchs(
            datas,
        )
    return node


class IndexFilesBow:
    def __init__(self, K: int = 2, L: int = 3) -> None:
        self.K = K if K > 1 else 2
        self.L = L if L > 1 else 2
        self.trees = {}

    def construct(self, patch_datas: list, hashcodes: list):
        result = regroup_datas(patch_datas, hashcodes)
        self.trees = {
            hashcode: TreeBow(racine=hierarchicalBOW(data, depth=self.L, K=self.K))
            for hashcode, data in result.items()
        }

    def getDuplicatesDatas(self, features_patch, hashcode_patch: str):
        try:
            tree = self.trees[hashcode_patch]
            return tree.getDuplicatePatchs(features_patch)
        except KeyError:
            return None
