class simple_charpy:
    def __init__(self, corrected_energy: float, thickness: float, width: float):
        """Class for calculating the non-instrumented Charpy impact strength. 

        In general by using this class you can calculate both notched and unnotched samples. For notched you need to put
        remained width on notch place.

        For now it is only for non-instrumented tests

        Parameters
        ----------
        corrected_energy : float
            it it the energy absorbed by breaking the test specimen
        thickness : float
            thickness of the test specimen
        width : float
            width of the test specimen

        Examples
        --------
        FIXME: Add docs.

        """
        
        self.impact_strength=(corrected_energy)/(thickness*width)
