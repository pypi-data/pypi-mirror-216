import numpy as np
import matplotlib.pyplot as plt
from typing import Union
import importlib



class _engineering_values:
        def __init__(self,
                     width,
                     thickness,
                     name=None,
                     elongation_array: Union[list, np.array] =None,
                     force_array: Union[list, np.array] =None,
                     force_units="N",
                     length_units="mm",
                   norm="ISO527"
                     ):
            global properties
            properties = importlib.import_module(f".{norm}", package=__package__)
            """initializer of engineering values class

            This class is used to menage the properties of engineering values

            Parameters
            ----------
            name : str
                name for your sample

            Examples
            --------
            FIXME: Add docs.

            """
            
            self.name=name
            self.force_units = force_units
            self.length_units=length_units
            self.thickness=thickness,
            self.width=width
            self.stress, self.strain=None,None
        def _calculate(self,
                      thickness:float,
                      width:float,
                      elongation_array,
                      force_array,
                      ):
            """Calculates the engineering stress and strain

            This method is used to calculate engineering stress and strain from height

            Parameters
            ----------
            thickness : float
                smaller initial dimension of the rectangular cross-section in the central part of test specimen
            width : float
                larger initial dimension of the rectangular cross-section in the central part of the test specimen
            elongation_array : list
                list of the sample elongation
            force_array : list
                list of the forces from the machinge
            force_units : str
                Units used as force units. Newtons [N] by default. Use shorten strings, as it is used in output
            length : str
                Units used for lenght, mm by default. Use short strings, as they are used in output. If you wanna use percent, just use % sign or percent
            """
            

            if self.length_units=="%" or self.length_units=="percent":
                self.percent_strain=True
            else:
                self.percent_strain=False


            if  self.stress is  None and self.strain is None:
                initial_area=thickness*width
                self.stress=[force/initial_area for force in force_array]
                if self.percent_strain:
                    self.strain=[strain for strain in elongation_array]
                else:
                    self.strain=[strain*0.01 for strain in elongation_array]

            self.strength=self._calculate_strength(self.stress,
                                                  self.strain)
            
            self.at_break=self._calculate_at_break(self.strain,
                                                  self.stress)
            
            self.yield_strength=self._calculate_yield_strength(self.stress,
                                                              self.strain)
            self.tensile_modulus=self._calculate_tensile_modulus()

        class _calculate_strength:
            def __init__(self,strain: np.array,stress:np.array):
                """Strenght is according to ISO-527-1 first maximum local value

                Parameters
                ----------
                strain : np.array
                    strain array
                stress : np.array
                    stress array

                Examples
                --------
                FIXME: Add docs.

                """
                
                strength = properties.strenght(strain,stress)
                self.value=strength.value
                self.strain=strength.strain

        class _calculate_yield_strength:
            def __init__(self, stress: np.array, strain: np.array):
                """
                Yield strenght  is according to ISO-527-1 strain increase without stress increase. 

                Parameters
                ----------
                stress : np.array
                    stress numpy array
                strain : np.array
                    strain numpy array

                Examples
                --------
                FIXME: Add docs.

                """
                yield_strenght=properties.yield_strenght(stress, strain)
                self.stress, self.strain=yield_strenght.value,yield_strenght.strain
        class _calculate_at_break:
            """
            This class calculates values at the brain according to ISO 527-1
            """
            def __init__(self,stress, strain):
                at_break=properties.at_break(stress, strain)
                self.stress=at_break.stress
                self.strain=at_break.strain


        def _calculate_tensile_modulus(self,
                                      plot=False,
                                      r2=True,
                                      output=False,
                                      lower_limit=0.05,
                                      upper_limit=0.25
                                      ):
            """            Tensile, or Young's modulus is the slope of strain/stress curve, between strains equals to 0.05 and 0.25 percent according to DIN ISO 527-1

            Parameters
            ----------
            plot : bool
                Put True for use pyplot on the tensile modulus part
            r2 : Put coeffitient 	of determination into pyplot label
                Put coeffitient of determination into pyplot label
            output : bool
                Print the output of this method
            lower_limit : float
                lower limit of the measurement boundary
            upper_limit : float
                upper limit of the measurement boundary

            Examples
            --------
            FIXME: Add docs.

            """

            E=properties.tensile_modulus(self.stress,
                                         self.strain,
                                         percent_strain=self.percent_strain
                                         )
            if plot:
                label=rf"Young's modulus {int(E.tensile_modulus)} $\left[\frac{{{self.force_units}}}{{{self.length}^2}}\right]$"
                if r2:
                    label+="\n"+rf"$R^{{{2}}}={E.r2}$"
                    plt.plot(E.module_strain,
                             E.module_stress,
                             label=label
                             )
            if output:
                print(f"Tensile modulus is equal to {int(E.tensile_modulus)} [{self.force_units}/{self.length}^2]")
            return   E.tensile_modulus

                
        def set(self,
                engineering_stress: Union[list, np.array] =None,
                engineering_strain:Union[list, np.array] =None,
                # TODO: gives TypeError: only size-1 arrays can be converted to Python scalars while using numpy array
                # TODO: gives KeyKerrr None
                # TODO: in general this method does not work yet!
                ):
            """Method to set engineering stress and engineering strain

            Parameters
            ----------
            engineering_stress : list
                array of engineering stress
            engineering_strain : list
                array of engineering strain

            Examples
            --------
            FIXME: Add docs.

            """
            
            self.stress, self.strain=engineering_stress, engineering_strain
            self._calculate(thickness=self.thickness,
                           width=self.width,
                           elongation_array=None,
                           force_array=None)
            

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
            plt.plot(self.strain,self.stress, label=self.name)
            plt.title(self.name)
            plt.ylabel(rf"Stress $\left[\frac{{{self.force_units}}}{{{self.length_units}^2}}\right]$")
            plt.xlabel(f"Strain [{self.length_units}]")
            plt.legend()
            if show:
                plt.show()

class _real_values(_engineering_values):

        def __init__(self,
                     name,
                     thickness,
                     width,
                     stress,
                     strain,
                     force_units,
                     length_units,
                     ):
            self.force_units=force_units
            self.length_units=length_units
            if length_units=="%" or length_units=="percent":
                self.percent_strain=True
            else:
                self.percent_strain=False

    
            _engineering_values.__init__(self,
                                        name=name,
                                        thickness=thickness,
                                        width=width
                                        )
            self.name=name + " [real]"
            width=self.width
            thickness=self.thickness
            super().__init__(self,
                             name=self.name,
                             thickness=self.thickness
                             )
            self._calculate(stress, strain)

        def _calculate(self, stress, strain):
            """
                Calculates the true stress and strain, from engineering values.
                Read more there:
                        https://courses.ansys.com/index.php/courses/topics-in-metal-plasticity/lessons/how-to-define-a-multilinear-hardening-plasticity-model-lesson-1/
            
                Parameters:
                        strain (array-like): An array of strain values.
                        stress (array-like): An array of corresponding stress values.
                        n: An count of chunks to divide stress/strain array
            
                Returns:
                    A tuple (start_strain, end_strain) representing the proportional range of the stress-strain curve.
            """
            self.stress=[stress_val*(1+strain_val) for stress_val, strain_val in zip(stress, strain)]
            self.strain=[np.log(1+strain_val) for strain_val in strain]

            self.strength=self._calculate_strength(self.stress,
                                                  self.strain)
            
            self.at_break=self._calculate_at_break(self.strain,
                                                  self.stress)
            
            self.yield_strength=self._calculate_yield_strength(self.stress,
                                                              self.strain)
            self.tensile_modulus=self._calculate_tensile_modulus()            






class _tensile:
    
    def __init__(self,
                 name: str,
                 thickness: Union[float, int],
                 width: Union[float, int],
                 elongation_array: Union[list, np.array] = None,
                 force_array: Union[list, np.array] = None,
                 stress_array: Union[list, np.array] = None,
                 strain_array: Union[list, np.array] = None,
                 force_units: str = "N",
                 length_units: str = "mm"
                 ):
        self.name, self.thickness, self.width=name, thickness, width
        self.engineering_values = _engineering_values(
            width=width,
            thickness=thickness,
            name=name,
            elongation_array=elongation_array,
            force_array=force_array,
            force_units=force_units,
            length_units=length_units
        )
        self.force_units, self.length_units = force_units, length_units
        self.stress_units = f"{force_units}/{length_units}^2"
        self.strain_units = f"{length_units}/{length_units}"
        if stress_array is None and strain_array is None:
            if elongation_array is None and force_array is None:
                raise ValueError("None of elongation/force or stress/strain arrays are defined!")
            elif thickness is None:
                raise ValueError("Thickness is not defined!")
            elif width is None:
                raise ValueError("Width is not defined!")
            else:
                self.elongation_array = elongation_array
                self.force_array = force_array
                self.engineering_values._calculate(thickness, width, elongation_array, force_array)
        else:
            self.engineering_values.set(stress_array, strain_array)

    def convert2real(self):
        self.real_values = _real_values(self.name,
                                        self.thickness,
                                        self.width,
                                        self.engineering_values.stress,
                                        self.engineering_values.strain,
                                        self.force_units,
                                        self.length_units)


