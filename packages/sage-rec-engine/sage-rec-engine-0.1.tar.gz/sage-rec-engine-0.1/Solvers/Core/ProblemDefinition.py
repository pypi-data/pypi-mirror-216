import json
import numpy
from Solvers.Core.Restrictions.RestrictionConflicts import (
    RestrictionConflict,
    RestrictionAlphaOrBeta,
)
from Solvers.Core.Restrictions.RestrictionDependences import (
    RestrictionOneToOneDependency,
    RestrictionOneToManyDependency,
    RestrictionManyToManyDependency,
    RestrictionManyToManyDependencyNew,
)
from Solvers.Core.Restrictions.RestrictionNumberOfInstances import (
    RestrictionUpperLowerEqualBound,
    RestrictionRangeBound,
    RestrictionFullDeployment,
    RestrictionRequireProvideDependency,
)
from Solvers.Core.Component import Component
from Solvers.Core.conflictGraph import getMaxClique
import logging


class ManeuverProblem:
    def __init__(self):
        self.VM_MaxLoad = 20
        self.componentsList = {}  # list of components
        self.restrictionsList = []  # list of restrictions
        self.IpInfo = {}  # list with other information
        self.applicationName = None

        logging.basicConfig()

        self.logger = logging.getLogger("maneuverApp")
        self.priceOffersFile = None
        self.nrComp = 0
        self.nrVM = 0
        self.one_to_one_dependencies = []
        self.max_clique = []

    def init(self, nr_vm, nr_comp):  # used at initilization for test instances
        self.nrVM = nr_vm
        self.nrComp = nr_comp
        self.R = numpy.zeros((self.nrComp, self.nrComp), dtype=int)  # conflicts graph
        self.D = numpy.zeros((self.nrComp, self.nrComp), dtype=int)  # corelation hraph

    # def solveLIP(self, choosing_stategy, solutions_limit):
    #     """
    #     Start solving the problem using the chosen solver and available configurations for VM
    #     :param cpSolver: Solver choosed to solve the problem
    #     :return:
    #     """
    #     self.logger.info("Resolve problem using CP solver")
    #     from maneuverRecomadEngine.exactsolvers import CP_Solver_GOT
    #     cpSolver = CP_Solver_GOT_LP.CP_Solver_GOT_LP(choosing_stategy, self)
    #
    #     for restriction in self.restrictionsList:
    #         restriction.generateRestrictions(cpSolver)
    #
    #     return cpSolver.run()

    def findPartitionsBasedOnConflictsMatrix(self):  # inspired from tarjan algorithm
        visitedComponents = {}
        for i in range(self.nrComp):
            visitedComponents[i] = False

        # print("visitedComponents", visitedComponents)
        # print(self.R)
        partitions = [[]]
        for i in range(self.nrComp):
            if visitedComponents[i]:
                continue
            visitedComponents[i] = True

            # print(i, "visitedComponents", visitedComponents)
            for partition in partitions:
                inConflic = False  # in conflict cu cele din partitia curenta
                for j in partition:
                    if self.R[i][j] == 1:
                        inConflic = True

                        # print("conflict direct", i, j, partition)

                    else:  # uitatate sa nu fie in conflict cu cele colocate
                        for compId in self.componentsList[j].dependenceComponentsList:
                            if self.R[i][compId] == 1:
                                inConflic = True
                                # print("conflict dependences", i, j, partition)
                                break
                if not inConflic:
                    partition.append(i)
                    break
            else:
                partitions.append([i])
            # print(i, partitions)

        # print("!!!!!!!!!!!!!!!", partitions)
        return partitions

    def solveCPNrOfInstances(self, choosing_stategy, solutions_limit):
        """
        Start solving components number problem using the chosen solver and available configurations for VM
        :param cpSolver: Solver chouse to solve the problem
        :return:
        """
        self.logger.info(
            "Find number of needed virtual machines based on components number restrictions"
        )
        from Solvers.Core.CP_Solver_Number_of_Instances import (
            CP_Solver_Got_Nr_Instances,
        )

        cpSolver = CP_Solver_Got_Nr_Instances(self, choosing_stategy, solutions_limit)

        for restriction in self.restrictionsList:
            restriction.generateRestrictions(cpSolver)

        return cpSolver.run()

    def readConfiguration(self, jsonFilePath, offers_list, inst):
        """
        Open json file that contains problem configurations and fills problem data
        :param jsonFilePath: the path to JSON file
        :return:
        """
        with open(jsonFilePath) as json_data:
            dictionary = json.load(json_data)
            self.logger.info(dictionary)
        self.readConfigurationJSON(dictionary, offers_list, inst)

    def readConfigurationJSON(self, dictionary, offers_list, inst):
        """
        Fills problem data from a dictionary
        :param dictionary: a dictionary that contains the problem description
        :return:
        """
        self.applicationName = dictionary["application"]
        for component in dictionary["components"]:
            self._addComponent(component)

        self.init(len(self.componentsList), len(self.componentsList))

        orComponents = set()
        for restriction in dictionary["restrictions"]:
            if inst != 0:
                if restriction["type"] == "LowerBound" and restriction["bound"] == -1:
                    restriction["bound"] = inst
                    self.wpInst = inst

            for comp in self._addRestriction(restriction):
                orComponents.add(comp)

        self.nrComp = len(self.componentsList)

        self.IpInfo = dictionary["IP"]

        # add restriction OS
        self.__addOperationSystemRestriction()

        # add information about minimum number of instances of each component
        self.__addRestrictionsComponentsNumber(orComponents)

        self.nrVM = self.__finidInitialNumberOfVMs(False)

        # add other useful information for EA alg
        #  -- like number of conflicts that a component is in
        self.__addInformationForEA()

        # add restriction that fixes some components on VMs

        self.__find_conflict_elements_clique(orComponents)

        self.offers_list = offers_list

    def __addInformationForEA(self):
        for i in range(self.nrComp):
            for j in range(self.nrComp):
                if self.R[i][j] == 1:
                    self.componentsList[i].conflictComponentsList.add(j)
            self.componentsList[i].numberOfConflictComponents = len(
                self.componentsList[i].conflictComponentsList
            )
        for i in range(self.nrComp):
            for j in range(self.nrComp):
                if self.D[i][j] == 1:
                    self.componentsList[i].dependenceComponentsList.add(j)

    def __finidInitialNumberOfVMs(self, useMinBinNr=False):
        """
        Calculates the initial number of VMs used for solution  building. By default it finds the minimum number of
        instances for each component based on the restrictions that are related to components number
        :param useMinBinNr: beside the default value, the minimum number of bins is added. It is calculated based on
        restrictions related to components conflicts
        :return: number of VM
        """

        # print("useMinBinNr", useMinBinNr)
        runningTime, components = self.solveCPNrOfInstances("LOWEST_MIN_MIN", 10000)
        for compId, comp in self.componentsList.items():
            comp.minimumNumberOfInstances = components[compId]

        minimumBins = self.findPartitionsBasedOnConflictsMatrix()
        # print("Bin:", minimumBins)

        __vmNr = numpy.sum(components)
        if useMinBinNr:
            __vmNr += len(minimumBins)
        return __vmNr

    def __addRestrictionsComponentsNumber(self, orComponents):
        """
        Adds restriction regarding the fact that at least one component should be deployed.
        The components that are not in 'OR' relation should be deployed alt least one time.
        :param orComponents: list of components in 'OR' relation
        :return:
        """
        all_comps = set()
        for component in self.componentsList:
            all_comps.add(component + 1)
        all_comps = all_comps.difference(orComponents)

        # print ("all_comps", all_comps)
        # print ("orcomps", orComponents)
        # print ("componentsList", self.componentsList)
        for compId in all_comps:
            self.restrictionsList.append(
                RestrictionUpperLowerEqualBound([compId], ">=", 1, self)
            )

    def __addOperationSystemRestriction(self):
        """
        Add conflict restriction induced by the fact that different components need different operating system.
        The restriction is induced by the fact that the user is not adding explicit restrictions
        :return:
        """
        dict = {}
        for comp in self.componentsList:
            if not (
                (self.componentsList[comp].operatingSystem is None)
                or (len(self.componentsList[comp].operatingSystem) == 0)
            ):
                if self.componentsList[comp].operatingSystem in dict:
                    dict[self.componentsList[comp].operatingSystem].append(comp)
                else:
                    dict[self.componentsList[comp].operatingSystem] = [comp]
        self.logger.debug("Operating system of the components: {}".format(dict))
        dict2 = dict.copy()
        if len(dict) > 1:
            for i in dict:
                dict2.pop(i, None)
                for j in dict2:
                    for k in dict[i]:
                        self.restrictionsList.append(
                            RestrictionConflict(k + 1, [u + 1 for u in dict2[j]], self)
                        )

    def __get_graph_components(self, or_components):
        components = {}

        startIndex = 0
        for comp_id in range(len(self.R)):
            if comp_id + 1 not in or_components:
                components[comp_id] = []

                # Appending each instance as a standalone node
                for i in range(
                    startIndex,
                    startIndex
                    + self.componentsList[comp_id].getMinimumPossibleNumberOfInstances(
                        self.componentsList
                    ),
                ):
                    components[comp_id].append(i)
                startIndex += self.componentsList[
                    comp_id
                ].getMinimumPossibleNumberOfInstances(self.componentsList)
            else:
                try:
                    if self.wpInst >= 8 and comp_id == 3:
                        components[comp_id] = []

                        # Appending each instance as a standalone node
                        for i in range(
                            startIndex,
                            startIndex
                            + self.componentsList[
                                comp_id
                            ].getMinimumPossibleNumberOfInstances(self.componentsList),
                        ):
                            components[comp_id].append(i)
                        startIndex += self.componentsList[
                            comp_id
                        ].getMinimumPossibleNumberOfInstances(self.componentsList)
                except NameError:
                    wpInst = 0

        conflicts = {}

        for comp_id in components.keys():
            conflicts[comp_id] = []

            for comp_id2 in range(len(self.R)):
                if self.R[comp_id][comp_id2] == 1 and comp_id2 in components.keys():
                    conflicts[comp_id].append(comp_id2)

        return components, conflicts

    def __find_conflict_elements_clique(self, or_components):
        elements = self.__get_graph_components(or_components)

        # components = []
        # G = nx.Graph()

        # for comp_id in range(len(self.R)):
        #     if (comp_id + 1) not in or_components:
        #         components.append(comp_id)
        #         G.add_node(comp_id)

        # for index_node_id1 in range(len(components) - 1):
        #     for index_node_id2 in range(index_node_id1 + 1, len(components)):
        #         #print(components[index_node_id1], components[index_node_id2])
        #         if self.R[components[index_node_id1]][components[index_node_id2]] == 1:
        #             #print("__________edge: ", index_node_id1,index_node_id2)
        #             G.add_edge(components[index_node_id1], components[index_node_id2])

        # cliques = nx.find_cliques(G)

        # max_comp_number = 0
        # max_clique =[]
        # for clique in cliques:
        #     s = 0
        #     for comp_id in clique:
        #         s += self.componentsList[comp_id].getMinimumPossibleNumberOfInstances(self.componentsList)
        #     if max_comp_number < s:
        #         max_comp_number = s
        #         max_clique = clique
        # print("cliques ------", clique, s)

        # print("clique", max_clique, max_comp_number)

        max_clique = getMaxClique(elements)
        # print(max_clique)

        self.max_clique = max_clique

    def _addComponent(self, comp_dictionary):
        """
        From json description of the component extract the properties and stores them into a instance of Component class
        :param comp_dictionary: a dictionary loaded from json component description
        :return:
        """
        id = comp_dictionary["id"] - 1

        c = Component(
            id,
            comp_dictionary["name"] if "name" in comp_dictionary else None,
            comp_dictionary["Compute"]["CPU"]
            if "CPU" in comp_dictionary["Compute"]
            else None,
            comp_dictionary["Compute"]["GPU"]
            if "GPU" in comp_dictionary["Compute"]
            else "false",
            comp_dictionary["Compute"]["Memory"]
            if "Memory" in comp_dictionary["Compute"]
            else None,
            comp_dictionary["Storage"]["StorageSize"]
            if "StorageSize" in comp_dictionary["Storage"]
            else None,
            comp_dictionary["Storage"]["StorageType"]
            if "StorageType" in comp_dictionary["Storage"]
            else None,
            comp_dictionary["Storage"]["StorageValue"]
            if "StorageValue" in comp_dictionary["Storage"]
            else None,
            comp_dictionary["Network"]["dataIn"]
            if "dataIn" in comp_dictionary["Network"]
            else None,
            comp_dictionary["Network"]["dataOut"]
            if "dataOut" in comp_dictionary["Network"]
            else None,
            comp_dictionary["Network"]["networkConnections"]
            if "networkConnections" in comp_dictionary["Network"]
            else None,
            comp_dictionary["keywords"] if "keywords" in comp_dictionary else None,
            comp_dictionary["operatingSystem"]
            if "operatingSystem" in comp_dictionary
            else None,
        )

        self.componentsList[id] = c

    def _addRestriction(self, dictionary):
        """
        From json description extracts the restrictions (conflict, multiplicity and dependency between components
        :param restrictionDictionary: From json description of the components restrictions
        :return:
        """

        # print("dictionary ", dictionary)
        dictionaryOrRelation = set()
        restrictionType = dictionary["type"]
        if restrictionType == "Conflicts":
            self.restrictionsList.append(
                RestrictionConflict(
                    dictionary["alphaCompId"], dictionary["compsIdList"], self
                )
            )

        elif restrictionType == "OneToOneDependency":
            self.restrictionsList.append(
                RestrictionOneToOneDependency(
                    dictionary["alphaCompId"], dictionary["betaCompId"], self
                )
            )
            self.__fill_one_to_one_dependency_list(
                dictionary["alphaCompId"], dictionary["betaCompId"]
            )
        elif restrictionType == "ManyToManyDependency":
            self.restrictionsList.append(
                RestrictionManyToManyDependency(
                    dictionary["alphaCompId"],
                    dictionary["betaCompId"],
                    dictionary["sign"],
                    self,
                )
            )
        elif restrictionType == "ManyToManyDependencyNew":
            self.restrictionsList.append(
                RestrictionManyToManyDependencyNew(
                    dictionary["alphaCompId"],
                    dictionary["betaCompId"],
                    dictionary["n"],
                    dictionary["m"],
                    self,
                )
            )
        elif restrictionType == "OneToManyDependency":
            self.restrictionsList.append(
                RestrictionOneToManyDependency(
                    dictionary["alphaCompId"],
                    dictionary["betaCompId"],
                    dictionary["number"],
                    self,
                )
            )
        elif restrictionType == "RangeBound":
            self.restrictionsList.append(
                RestrictionRangeBound(
                    dictionary["compsIdList"],
                    dictionary["lowerBound"],
                    dictionary["upperBound"],
                    self,
                )
            )
            self.__componentAddNumberOfInstancesDependences(dictionary["compsIdList"])
        elif restrictionType == "UpperBound":
            self.restrictionsList.append(
                RestrictionUpperLowerEqualBound(
                    dictionary["compsIdList"], "<=", dictionary["bound"], self
                )
            )
            self.__componentAddNumberOfInstancesDependences(dictionary["compsIdList"])
        elif restrictionType == "LowerBound":
            self.restrictionsList.append(
                RestrictionUpperLowerEqualBound(
                    dictionary["compsIdList"], ">=", dictionary["bound"], self
                )
            )
            self.__componentAddNumberOfInstancesDependences(dictionary["compsIdList"])
        elif restrictionType == "EqualBound":
            self.restrictionsList.append(
                RestrictionUpperLowerEqualBound(
                    dictionary["compsIdList"], "=", dictionary["bound"], self
                )
            )
            self.__componentAddNumberOfInstancesDependences(dictionary["compsIdList"])
        elif restrictionType == "FullDeployment":
            self.restrictionsList.append(
                RestrictionFullDeployment(
                    dictionary["alphaCompId"], dictionary["compsIdList"], self
                )
            )
        elif restrictionType == "FullDeployment1":
            full_deploy_compIds = dictionary["compsIdList"]
            for comp_id in full_deploy_compIds:
                # find conflict list
                conflicts_list = []
                for i in range(self.nrComp):
                    if self.R[i][comp_id - 1] == 1:
                        conflicts_list.append(i + 1)
                # add actual constain
                self.restrictionsList.append(
                    RestrictionFullDeployment(comp_id, conflicts_list, self)
                )
        elif restrictionType == "RequireProvideDependency":
            self.restrictionsList.append(
                RestrictionRequireProvideDependency(
                    dictionary["alphaCompId"],
                    dictionary["betaCompId"],
                    dictionary["alphaCompIdInstances"],
                    dictionary["betaCompIdInstances"],
                    self,
                )
            )
        elif restrictionType == "AlternativeComponents":
            self.restrictionsList.append(
                RestrictionAlphaOrBeta(
                    dictionary["alphaCompId"], dictionary["betaCompId"], self
                )
            )
            dictionaryOrRelation.add(dictionary["alphaCompId"])
            dictionaryOrRelation.add(dictionary["betaCompId"])

        return dictionaryOrRelation

    def __fill_one_to_one_dependency_list(self, alpha_component_id, beta_component_id):
        """
        Function create a list with one to one dependency relations between components
        :parameter alpha_component_id: first component id
        :parameter beta_component_id: second component id
        """
        alpha_component_id -= 1
        beta_component_id -= 1
        found = False
        for dependency_group in self.one_to_one_dependencies:
            if (
                alpha_component_id in dependency_group
                or beta_component_id in dependency_group
            ):
                dependency_group.add(alpha_component_id)
                dependency_group.add(beta_component_id)
                found = True
        if not found:
            self.one_to_one_dependencies.append({alpha_component_id, beta_component_id})

    def __componentAddNumberOfInstancesDependences(self, components):
        if len(components) == 1:
            return
        # transform to iternal notation from 0 to n-1
        # print("before components:", components)
        for i in range(len(components)):
            components[i] -= 1
        # print("components:",components)
        for comp_id in components:
            self.componentsList[comp_id].numberOfInstancesDependences.update(components)
            self.componentsList[comp_id].numberOfInstancesDependences.remove(comp_id)

    def __repr__(self):
        for i in self.componentsList:
            print(i)
        return str(self.componentsList)

    def _getComponentsHardwareRestrictions(self):
        """
        Resturns a list with hardware restriction for each component
        :return:
        """
        # print("len(self.componentsList)", len(self.componentsList))
        return [
            self.componentsList[compId].getComponentHardWareResources()
            for compId in range(0, len(self.componentsList))
        ]

    def compareComponentsRegardingHardwareRestrictions(self, compAlphaId, compBetaId):
        """
        Finds which component alpha or beta needs more hardware resources
        :param compAlphaId: alpha component id
        :param compBetaId: beta component id
        :return: sumAlpha - in how many cases component alpha needs less resources that component beta
                 sumBeta - in how many cases component beta needs less resources that component alpha
        """
        compAlpha = self.componentsList[compAlphaId]
        compBeta = self.componentsList[compBetaId]
        sumAlpha = (
            0  # add 1 if alpha component need less resources then beta components
        )
        sumBeta = 0  # add 1 if beta component need less resources then alpha components
        retAlpha, retBeta = self.__compareResource(compAlpha.HM, compBeta.HM)
        sumAlpha += retAlpha
        sumBeta += retBeta

        retAlpha, retBeta = self.__compareResource(compAlpha.HC, compBeta.HC)
        sumAlpha += retAlpha
        sumBeta += retBeta

        retAlpha, retBeta = self.__compareResource(compAlpha.HS, compBeta.HS)
        sumAlpha += retAlpha
        sumBeta += retBeta

        retAlpha, retBeta = self.__compareResource(compAlpha.NIn, compBeta.NIn)
        sumAlpha += retAlpha
        sumBeta += sumBeta

        retAlpha, retBeta = self.__compareResource(compAlpha.NOut, compBeta.NOut)
        sumAlpha += retAlpha
        sumBeta += retBeta

        retAlpha, retBeta = self.__compareResource(
            compAlpha.NConnections, compBeta.NConnections
        )
        sumAlpha += retAlpha
        sumBeta += retBeta
        return sumAlpha, sumBeta

    def __compareResource(self, alphaValue, betaValue):
        """
        Compare 2 hardware resources to which component alpha or beta needs more resources
        :param alphaValue: alpha component resource value
        :param betaValue: beta component resource value
        :return: retAlpha - 1 if component alpha needs more resources that component beta, 0 otherwais
                 retBeta - 1 if component beta needs more resources that component alpha, 0 otherwais
        """
        retAlpha = 0
        retBeta = 0
        if (alphaValue is None) and (betaValue is None):
            return retAlpha, retBeta
        if (alphaValue is None) and (betaValue is not None):
            if betaValue.HM > 0:
                retAlpha = 1
        elif (betaValue is None) and (alphaValue is not None):
            if alphaValue > 0:
                retBeta = 1
        return retAlpha, retBeta

    def buildInitialAllocation(self):
        """
        Helper function used to build an allocation maxim that deploys each component on a different VM.
        Used to create an initial query in order to extract all valid offers
        :return: an allocation matrix with all different components deployed on a different VM (without taken in
        consideration any constraints)
        """
        a = numpy.zeros((self.nrComp, self.nrComp))
        for i in range(self.nrComp):
            a[i][i] = 1
        return a

    def buildSolutinInformations(self, allocation_matrix, vms_number):
        """
        Builds the dictionary for json query for offers
        :param allocation_matrix: the allocation matrix of components to VM
        :param vms_number: VMs number
        :return: a dictionary for
        """

        result = {}

        for k in range(vms_number):
            s = 0
            for i in range(self.nrComp):
                if allocation_matrix[i][k] == 1:
                    s += 1
            if s == 0:
                continue

            memory = 0

            cpus = 0
            gpus = 0
            cpusType = set()

            storageHDD = 0
            storageSSD = 0
            storageType = set()

            # netConnections = 0
            netConections = set()
            netDataIn = 0
            netDataOut = 0

            keywords = set()
            operatingSystem = set()

            for i in range(self.nrComp):
                __component = self.componentsList[i]
                if allocation_matrix[i][k] == 1:
                    # memory
                    memory += int(__component.HM) if __component.HM is not None else 0
                    # cpu
                    __cpuType = int(__component.HCType)
                    if __cpuType is None or __cpuType == "false":
                        cpusType.add("CPU")
                        __cpuType = "CPU"
                    else:
                        cpusType.add("GPU")
                        __cpuType = "GPU"
                    if __cpuType == "CPU":
                        cpus += int(__component.HC) if __component.HC is not None else 0
                    else:
                        gpus += int(__component.HC) if __component.HC is not None else 0
                    # storage
                    __storageType = __component.HSType
                    if __storageType == "SSD":
                        storageType.add("SSD")
                        __storageType = "SSD"
                    else:
                        storageType.add("HDD")
                        __storageType = "HDD"
                    if __storageType == "HDD":
                        storageHDD += (
                            __component.HS if __component.HS is not None else 0
                        )
                    else:
                        storageSSD += (
                            __component.HS if __component.HS is not None else 0
                        )
                    # network
                    # netConnections += __component.NConnections if __component.NConnections is not None else 0
                    # netDataIn += __component.NIn if __component.NIn is not None else 0
                    # netDataOut += __component.NOut if __component.NOut is not None else 0

                    netConections = (
                        __component.NConnections
                        if __component.NConnections is not None
                        else ""
                    )

                    # keywords
                    for key in __component.keywords:
                        keywords.add(key)
                    # OS
                    operatingSystem.add(__component.operatingSystem)
            result[str(k)] = {
                "memory": memory,
                "cpu": {"type": list(cpusType), "cpu": cpus, "gpu": gpus},
                "storage": {
                    "type": list(storageType),
                    "hdd": storageHDD,
                    "ssd": storageSSD,
                },
                "network": {
                    "connections": netConections,
                    "dataIn": netDataIn,
                    "dataOut": netDataOut,
                },
                "keywords": list(keywords),
                "operatingSystem": list(operatingSystem),
            }

            # neededVM += 1
            result["IP"] = self.IpInfo
        # print("result:", result, "\n")
        return result
