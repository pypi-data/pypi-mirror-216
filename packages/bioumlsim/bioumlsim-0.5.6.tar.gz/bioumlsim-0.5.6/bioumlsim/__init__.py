import jpype
import jpype.imports
import numpy as np
import pandas as pd
import os
import platform
import subprocess
from os import path as ospath

class BioUMLSim:
    
    bioUMLPath = None
    atol = 1E-8
    rtol = 1E-8
    engine = None

    def getJVMVersion(self):
        return '.'.join(map(str, jpype.getJVMVersion()))
        
    def checkJDKVersion(self, release):
        if not os.path.isfile(release):
            return False
        f = open(release,'r')
        lines = f.readlines()
        for line in lines :
            if line.startswith('JAVA_VERSION=\"1.8') or line.startswith('JAVA_VERSION=\"11'):
                return True
        return False
    
    def isMac(self):
        systemName = platform.system()
        if systemName == 'Windows' or systemName == 'Linux':
            return False
        return True
  
    def findJDK(self, verbose=False):
        jdkBasePath = ospath.join(ospath.expanduser("~"), ".jdk")
        if not os.path.isdir(jdkBasePath):
            print('Can not find appropriate JDK in '+jdkBasePath)
            return ''              
        for name in os.listdir(jdkBasePath):
            jdkPath = ospath.join(jdkBasePath, name)
            if self.isMac():
                jdkPath = ospath.join(jdkPath,'Contents', 'Home')
            if verbose:
                print('Checking '+ospath.join(jdkPath,'release'))
            if self.checkJDKVersion(ospath.join(jdkPath,'release')):
                if verbose:
                    print('Appropriate version detected')
                return jdkPath
        print('Can not find appropriate JDK in '+jdkBasePath)
        return '' 
         
    def findJVM(self, jdkLocation = '', verbose=False):
        jdk = jdkLocation
        if jdk == '':
            jdk = self.findJDK(verbose=verbose)
        if jdk == '':
            return jdk
        if verbose:
            print('JDK found at ' + jdk)
        possiblePaths = self.guessJVMLocations()
        for possiblePath in possiblePaths:
            jvm = ospath.join(jdk, possiblePath)
            print ('Check JVM location: '+jvm)
            if ospath.isfile(jvm):
                print ('JVM Found')
                return jvm;
        print('Can not find appropriate JVM. Please install 1.8 or 11 Java')
        return '' 
    
    def guessJVMLocations(self):
        systemName = platform.system()
        if systemName == 'Windows':
            return ['jre/bin/server/jvm.dll','bin/server/jvm.dll']
        elif systemName == 'Linux':
            return ['lib/server/libjvm.so','jre/lib/amd64/server/libjvm.so']
        else:
            return ['jre/lib/server/libjvm.dylib', 'lib/server/libjvm.dylib',
                    'jre/lib/jli/libjvm.dylib']
    
    def isJavaSet(self):
         try:
             p = subprocess.check_output(["java", "-version"], stderr=subprocess.STDOUT)
             version = str(p.splitlines()[0].split()[-1])[3:]
             return version.startswith('1.8') or version.startswith('11')
         except FileNotFoundError:
             return False 
    
    def isJavaHomeSet(self, verbose=False):
        try:
            os.environ['JAVA_HOME']
            if verbose:
                print('Java home: '+os.environ['JAVA_HOME'])
            return True
        except KeyError:
            return False
     
    def __init__(self, jdk = '', verbose = False):
        path = ospath.join(ospath.dirname(__file__),'jars')
        if verbose:
            print('Path to java classes: '+path)
            print('Path to jdk: '+jdk)
        self.bioUMLPath = path
        if jdk != '':
            jvmPath = self.findJVM(jdkLocation = jdk, verbose=verbose)
        elif self.isJavaSet() and self.isJavaHomeSet(verbose=verbose):    
            jvmPath = ''
        else:
            jvmPath = self.findJVM(verbose=verbose)
        if jvmPath == '':
           if verbose:
               print('Will try to find jvm automatically') 
           jpype.startJVM(classpath=[path+'/*'], convertStrings=True)
        else:
           if verbose:
               print ('JVM is located at '+jvmPath)
           jpype.startJVM(jvmPath, classpath=[path+'/*'], convertStrings=True)
        print("JVM version: "+self.getJVMVersion())

    def load(self, file, verbose = False):
        """
        Loads SBML file and transforms it into object which represents mathematical model.
        Args:
            file (str): path to file
        Returns:
            model
        """
        if verbose:
             print(f"SBML file is loading: {file}")
        diagram = jpype.JClass("biouml.plugins.sbml.SbmlModelFactory").readDiagram(file, False)
        self.engine = jpype.JClass("biouml.plugins.simulation.java.JavaSimulationEngine")()
        self.engine.setDiagram(diagram)
        self.engine.setClassPath(ospath.join(self.bioUMLPath,'src.jar'))
        if  not verbose:
            self.engine.disableLog()
        self.engine.setAbsTolerance(self.atol)
        self.engine.setRelTolerance(self.rtol)
        return Model(self.engine, self.engine.createModel())
    
    def plot(self, df):
        import matplotlib.pyplot as plt
        plt.plot(df)
        plt.show()
    
    def loadTest(self, verbose = False):
        path = ospath.join(ospath.dirname(__file__),'test.xml')
        return self.load(path, verbose=verbose)
         
class Model:
    
    def __init__(self, engine, model):
        self.engine = engine
        self.model = model
        
    def simulate(self, tend, numpoints, verbose = False):
        """
        Simulates SBML model and returns results.
        Args:
            tend: final time for simulation
            numpoints: number of time points
        Returns:
            simulation results
        """
        if (verbose):
            print(f"Simulating model: {self.engine.getDiagram().getName()}")
        self.engine.setCompletionTime(tend)
        self.engine.setTimeIncrement(tend / numpoints)
        result = self.engine.simulateSimple(self.model)
        species = self.engine.getFloatingSpecies()
        values = np.array(result.getValuesTransposed(species))
        names = np.array(species)
        times = np.array(result.getTimes());
        return pd.DataFrame(values, columns = names, index = pd.Index(times, name ="Time"))