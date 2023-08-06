import numpy as np
import matplotlib.pyplot as plt
from typing import Union
import importlib


"""
TODO:
Create  abstract class for properties like tensile strength, tensile modulus, etc, with pass, so using diffrent norms and materials will be easier
Move calculation of real values into method of engineering values
Add decorators

SOURCES:

https://professorkazarinoff.github.io/Engineering-Materials-Programming/07-Mechanical-Properties/mechanical-properties-from-stress-strain-curves.html


"""


class sample:
    """Initialization of sample class

    That's class for each of your tested sample

    Parameters
        ----------
        name : str
        name of your sample for example "Neat PLA"
        manufactured_method : str
        how your sample was made, etc. by FDM or injection method, just for description
        comments : str
        any comments describing your sample
    
    Examples
        --------
        elongation_array=df["elongation"]
        force_array=df["force"]

        # This uses N ewtons and mm by default to ensure [N/mm^2] as it is equal to MPa
        example=mt.sample(name="your sample name",
        thickness = 5,
        width= 5,
        elongation_array=elongation_array,
        force_array=force_array
        )
        """

    def __init__(self,name: str,
                 comments: str=None,
                 path: str= None,
                 manufactured_method: str=None):
            self.name=name
            self.comments=comments
        
    def define_tensile_test(self,
                            thickness:float = None,
                            width:float = None,
                            elongation_array: Union[list, np.array] =None,
                            force_array: Union[list, np.array] =None,
                            stress_array: Union[list, np.array] =None,
                            strain_array: Union[list, np.array] =None,
                            force_units: str="N",
                            length_units: str="mm",
                            material="polymers",
                            norm="ISO527"):
            """

    That's function to calculate tensile test parameters

    Parameters
        ----------
        thickness : float
        thickness of your sample
        width : float
        width of your sample
        elongation_array : Union[list, np.array]
        elongation array from your tensile machine
        force_array : Union[list, np.array]
        forces obtained from your tensile machine
        stress_array : Union[list, np.array]
        calculated stresses
        strain_array : Union[list, np.array]
        calculated strains
        force_units : str
        force units of your force array
        lenght_units : str
        length units of your force array

    Raises
        ------
        ValueError
        Raises ValueError while stress/strains or width/thickness are not defined
    
    Examples
        --------
        elongation_array=df["elongation"]
        force_array=df["force"]

        # This uses N ewtons and mm by default to ensure [N/mm^2] as it is equal to MPa
        example=mt.sample(name="your sample name",
        thickness = 5,
        width= 5,
        elongation_array=elongation_array,
        force_array=force_array
        )
        """

            self._test = importlib.import_module(".polymers.tensile", package=__package__)
            
            self.thickness, self.width= thickness,width
            self.tensile=self._test._tensile(name=self.name,
                                        elongation_array=elongation_array,
                                        force_array=force_array,
                                        force_units=force_units,
                                        length_units=length_units,
                                        stress_array=stress_array,
                                        strain_array=strain_array,
                                        thickness=thickness,
                                        width=width
                                        )


    def calculate_real_values(self):
        print(dir(self.tensile))
        # exit()
        self.real_vals=self.tensile.convert2real()
        # self.real_vals.calculate(self.eng_values.stress,
        #                            self.eng_values.strain)            
    def plot(self, show=False):
        """Method for plotting the results

            This method can be used to plot your engineering stress-strain curve. If you wanna show it instantly use
            parameter show as True

            Parameters
            ----------
            show : bool
                It it equal to matplotlib.pyplot function show

            Examples
            --------
            FIXME: Add docs.

            """
        plt.plot(self.elongation_array,self.force_array, label=self.name)
        plt.title(self.name)
        plt.ylabel(f"Force [{self.force_units}]")
        plt.xlabel(f"Strain [{self.lenght_units}]")
        plt.legend()
        if show:
                plt.show()        


                
        
    def composition_from_name(self, delimiter: str='-', percent_sign="p"):
        """Method to obtain material ingridiens from name, as I usually name files extracted from machine with code allowing me to get that information from filename. For example you can name you sample 10pFDM-20pPET, and it will mean there is 20percent of addition PET as well as 10 percent of Polyolefin Elastometer addition. It can be also 90pPC-10pPET.
        Parameters:
        delimiter: str
            It is the sign that delimits your composition, in default it is - sign.
        percent_sign: str
            It is the sign takes everything before as percent, like in example 90pPC, so int before (90) will be int in your composition.
        
    Returns: 
            Sets the composition variable into a dicts of your composition. For example from 90pPC-10pPET it will return a dict {PC: 90, PET: 10}
        """
        
        from .files import files
        name=self.name
        self.composition = files.find_composition(name, delimiter, percent_sign)
        return self.composition
        
    def modification_from_name(self, mods: list, place: int=0):
        """Function that finds if the sample was somehow modified, for example by thermal annealing

        This can be useful in case you are testing modified samples, and you marked your filename with the letter
        describing it.  By default describing letter is 

        Parameters
        ----------
        mods : list
            that is the list of potential modification you have used, for example A for annealing
        place : int
            That is placement of your describing letter in the modification name. By default it is 0,
        so for Annealing it will be A

        Examples
        --------
        FIXME: Add docs.

        """
        from files.files import find_modification
        self.modification = find_modification(self.name, mods, place)

    def method_from_name(methods: list, delimiter:str = '-'):
                    """Find the technique how the material was created

        Find the method how the material was created, what methods were used to modify it, etc. To do so it is using
        first letters of filename, so for extruded parts you can use EXT, for annealed extruded parts you can use aEXT
        etc.
                    For example if you obtained your material by FDM method containing 90pPET10prPET, you can use FDM-90pPET10prPET name, and it will set instance method variable to FDM

        Parameters
        ----------
        methods : list
            what methods you have used on your set
        delimiter : str
            what sign you wanna use to finish your method string. By default it is -

        Examples
        --------
        FIXME: Add docs.

        """


