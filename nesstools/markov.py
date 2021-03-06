import random as r


class MarkovModel(object):
    def __init__(self):
        self.model = []
        self.states = []
        self.durModel = []
        self.durStates = []

    def markovEventsFromStringData(self, strings):
        stringCount = len(strings)
        # format for events: [t, [f,f,f]]
        eventArray = []
        for s, string in enumerate(strings):
            for item in string:
                t = int(item[0])
                fret = int(item[1])
                exists = False
                for e in eventArray:
                    if t == e[0]:
                        # event found, so add this event to it
                        exists = True
                        e[1][s] = fret   # set the relevant fret, based on which string we're looking at
                        break
                if not exists:
                    newFrets = [-1 for i in range(stringCount)] # all null frets
                    newFrets[s] = fret                  # set the specific string fret
                    eventArray.append([t, newFrets])
        sortedEvents = sorted(eventArray, key=lambda x: x[0])
        return sortedEvents


    def generateMarkovStringModel(self, strings):
        events = self.markovEventsFromStringData(strings)
        prevArray = []
        prevIndex = 0
        prevDurIndex = 0
        for i in range(len(events)):
            elementIndex = 0
            t = events[i][0]
            frets = events[i][1]
            element = frets     # omitting duration for the moment
            if element in self.states:
                elementIndex = self.states.index(element)
            else:
                self.states.append( element )
                elementIndex = len(self.states) - 1
            if i > 0:
                connectionExists = False
                for item in self.model:
                    if prevIndex == item[0]:
                        if elementIndex == item[1]:
                            connectionExists = True
                            item[2] += 1
                if not connectionExists:
                    self.model.append([prevIndex, elementIndex, 1])
                
            durationIndex = 0
            
            if i > 0 and i < len(events)-1:
                if (i < len(events)-1):
                    dur = events[i+1][0] - t
                    if dur in self.durStates:
                        durationIndex = self.durStates.index(dur)
                    else:
                        self.durStates.append( dur )
                        durationIndex = len(self.durStates) - 1
                    if (i < len(events)-1):
                        durationConnectionExists = False
                        for item in self.durModel:
                            if prevDurIndex == item[0]:
                                if durationIndex == item[1]:
                                    durationConnectionExists = True
                                    item[2] += 1
                        if not durationConnectionExists:
                            self.durModel.append([prevDurIndex, durationIndex, 1])
                
            prevIndex = elementIndex
            prevDurIndex = durationIndex
            prevFrets = frets

    def generateSecondOrderMarkovStringModel(self, strings):
        events = self.markovEventsFromStringData(strings)
        prevArray = []
        prevIndex = 0
        prevDurIndex = 0
        frets = []
        prevFrets = []
        dur = 0
        prevDur = 0
        for i in range(len(events)-1):
            elementIndex = 0
            t = events[i][0]
            frets = events[i][1]
            if (i > 0):
                element = [prevFrets, frets]     # omitting duration for the moment
                if element in self.states:
                    elementIndex = self.states.index(element)
                else:
                    self.states.append( element )
                    elementIndex = len(self.states) - 1
                if i > 1:
                    connectionExists = False
                    for item in self.model:
                        if prevIndex == item[0]:
                            if elementIndex == item[1]:
                                connectionExists = True
                                item[2] += 1
                    if not connectionExists:
                        self.model.append([prevIndex, elementIndex, 1])
                
            durationIndex = 0
            
            if i > 1 and i < len(events)-1:
                if (i < len(events)-1):
                    dur = events[i+1][0] - t
                    durElement = [prevDur, dur]
                    if durElement in self.durStates:
                        durationIndex = self.durStates.index(durElement)
                    else:
                        self.durStates.append( durElement )
                        durationIndex = len(self.durStates) - 1
                    if (i < len(events)-1):
                        durationConnectionExists = False
                        for item in self.durModel:
                            if prevDurIndex == item[0]:
                                if durationIndex == item[1]:
                                    durationConnectionExists = True
                                    item[2] += 1
                        if not durationConnectionExists:
                            self.durModel.append([prevDurIndex, durationIndex, 1])
            
            prevIndex = elementIndex
            prevDurIndex = durationIndex
            prevFrets = frets
            prevDur = dur

    def generateThirdOrderMarkovStringModel(self, strings):
        events = self.markovEventsFromStringData(strings)
        prevArray = []
        prevIndex = 0
        prevDurIndex = 0
        frets = []
        prevFrets1 = []
        prevFrets2 = []
        dur = 0
        prevDur1 = 0
        prevDur2 = 0
        for i in range(len(events)-1):
            elementIndex = 0
            t = events[i][0]
            frets = events[i][1]
            if (i > 0):
                element = [prevFrets2, prevFrets1, frets]     # assemble element from 3 recent states, omitting duration for the moment
                # if it exists, get the id
                if element in self.states:
                    elementIndex = self.states.index(element)
                # if note, add it and set the index to the most recent element
                else:
                    self.states.append( element )
                    elementIndex = len(self.states) - 1
                # if we've got both previous states:
                if i > 2:
                    # if the two 3-state elements are already connected in the model
                    connectionExists = False
                    for item in self.model:
                        if prevIndex == item[0]:
                            if elementIndex == item[1]:
                                connectionExists = True
                                item[2] += 1
                    if not connectionExists:
                        self.model.append([prevIndex, elementIndex, 1])
            
            # DURATION MODEL
            durationIndex = 0
            if i > 2 and i < len(events)-1:
                if (i < len(events)-1):
                    dur = events[i+1][0] - t
                    durElement = [prevDur2, prevDur1, dur]
                    if durElement in self.durStates:
                        durationIndex = self.durStates.index(durElement)
                    else:
                        self.durStates.append( durElement )
                        durationIndex = len(self.durStates) - 1
                    if (i < len(events)-1):
                        durationConnectionExists = False
                        for item in self.durModel:
                            if prevDurIndex == item[0]:
                                if durationIndex == item[1]:
                                    durationConnectionExists = True
                                    item[2] += 1
                        if not durationConnectionExists:
                            self.durModel.append([prevDurIndex, durationIndex, 1])
            
            prevIndex = elementIndex
            prevDurIndex = durationIndex
            prevFrets2 = prevFrets1
            prevFrets1 = frets
            prevDur2 = prevDur1
            prevDur1 = dur


    def run(self, t, T, boredomThreshold=3, verbose=False, randomiseInitState=False):
        if verbose: print ("\n____________________\n\n ** running markov ** \n\n" )
        currentFretIndex = 0
        currentDurIndex = 0
        if randomiseInitState:
            currentFretIndex = self.model[r.randint(0, len(self.model)-1)][0]
            currentDurIndex = self.durModel[r.randint(0, len(self.durModel)-1)][0]
        output = []
        boredomFactor = 0
        boredomCount = 0
        prevState = -1
        while t < T:
            if verbose: print ("\nstep")
            nextFretIndex = self.nextStep(self.model, currentFretIndex)
            if (nextFretIndex == currentFretIndex): boredomFactor += 1
            else: boredomFactor = 0
            currentFretIndex = nextFretIndex
            if (boredomFactor >= boredomThreshold):
                currentFretIndex = r.randint(0, len(self.states)-1)
                if verbose: print ("BORED: choosing new index randomly "+str(currentFretIndex)+"\n")
                boredomFactor = 0
                boredomCount += 1
            frets = self.states[currentFretIndex]
            if verbose: print (frets)
            
            nextDurIndex = self.nextStep(self.durModel, currentDurIndex)
            currentDurIndex = nextDurIndex
            dur = self.durStates[currentDurIndex]


            if isinstance(dur, list):
                output.append( [t, frets[-1]] )
                t += dur[-1]
            else:
                output.append( [t, frets])
                t += dur
            #print(dur)
        if verbose: print("Run complete. I was bored %d time(s)" % boredomCount)
        return output

    def nextStep(self, inputModel, currentIndex):
        possibleSteps = []
        for m in inputModel:
            if m[0] == currentIndex:
                for i in range(m[2]):
                    # add one destination step to the list for each count listed in the model
                    # this will then weight a given step according to the 3rd value in the list
                    possibleSteps.append( m[1] )
        if (len(possibleSteps) > 0):
            nextStep = possibleSteps[r.randint(0, len(possibleSteps)-1)]
        else:
            nextStep = 0
        return nextStep

    def getTabLines(self, tabFile, stringCount=6, higherFrets=True):
        tab = ""
        tabLines = []
        if isinstance(tabFile, str):
            tab = open(tabFile, 'r')
            tabLines = self.tabLinesFromTextFile(tab, stringCount);
        else:
            tab = tabFile
            tabLines = [tab]

# string1 = [["1", '0'], ['3', '0'], ['4', '5'], ['5', '0']]
# string2 = [[1, 2], [2, 7], [3, 2], [5, 2]]
# string3 = [[1, 2], [5, 2]]

'''string1 = [["1", '0'], ['3', '0'], ['4', '5'], ['5', '0']]
string2 = [['1', '2'], ['2', '7'], ['3', '2'], ['5', '2']]
string3 = [['1', '2'], ['5', '2']]

strings = [string1, string2, string3]
# format for events: [t, [f,f,f]]
my_markov = MarkovModel();

#events = my_markov.markovEventsFromStringData(strings)
# format for markov = [[elmentIndex1, elmentIndex2, probability_int], [1, 5, 1], [1, 0, 2]] 
my_markov.generateSecondOrderMarkovStringModel(strings)
#print (events)

# TO DO:
# - allow training to be added in
# - allow model to be run and create score parameters
# - have a local variable for the models in the score?
# - have a separate class for the markov model?
output = my_markov.run(0, 10)

print (output)'''

