Library Layout
==============

Components
----------

This library contains everything needed to compute demodulation matrices. It has 4 main parts:

+-------------------------------------------------------------+--------------------------------------------------------------------------+
| Description                                                 | Code Thing                                                               |
+=============================================================+==========================================================================+
| A container for input data, :math:`\vec{I}_{obs}`           | `~dkist_processing_pac.input_data` package,                              |
|                                                             | specifically the                                                         |
|                                                             | `~dkist_processing_pac.input_data.dresser.Dresser`                       |
|                                                             | object                                                                   |
+-------------------------------------------------------------+--------------------------------------------------------------------------+
| Parameterized Mueller matrices for optical elements         | the `~dkist_processing_pac.optics` package                               |
+-------------------------------------------------------------+--------------------------------------------------------------------------+
| Objects to manage fitting parameters                        | `~dkist_processing_pac.fitter.fitter_parameters`                         |
| during fits and to return the final results                 | module, specifically the                                                 |
|                                                             | `~dkist_processing_pac.fitter.fitter_parameters.PolcalDresserParameters` |
|                                                             | object                                                                   |
+-------------------------------------------------------------+--------------------------------------------------------------------------+
| Process to collect all the pieces and actually run the fits | the `~dkist_processing_pac.fitter.polcal_fitter` module, specifically    |
|                                                             | the `~dkist_processing_pac.fitter.polcal_fitter.PolcalFitter` object     |
+-------------------------------------------------------------+--------------------------------------------------------------------------+

Let's take a look at each one:

Input Data
**********

The Dresser contains :math:`\vec{I}_{obs}` for every bin provided by the instrument pipeline. See SPEC-0213 for more detailed definitions.
In addition to containing the actual measured intensities, this object also contains information about the geometry of
the telescope (needed for computing :math:`\mathbf{M}_{12}` and :math:`\mathbf{M}_{36}`) and the configuration of the
Calibration Unit (needed for computing :math:`\mathbf{C}`).

Optics
******

The Telescope object contains the machinery necessary to compute :math:`\mathbf{M}_{12}` and :math:`\mathbf{M}_{36}`.
The actual matrices are accessed via the `Telescope.TM <dkist_processing_pac.optics.telescope.Telescope.TM>` property.
It can also compute the inverse telescope matrix via the
`Telescope.generate_inverse_telescope_model <dkist_processing_pac.optics.telescope.Telescope.generate_inverse_telescope_model>` method.

The `~dkist_processing_pac.optics.calibration_unit.CalibrationUnit` object contains the machinery necessary to compute
:math:`\mathbf{C}`, which is accessed via the `CalibrationUnit.CM <dkist_processing_pac.optics.calibration_unit.CalibrationUnit.CM>` property.

Parameters
**********

`~dkist_processing_pac.fitter.fitter_parameters.PolcalDresserParameters` contains fitting parameters for every bin
provided by the instrument pipeline. There is a 1-to-1-to-1 mapping between a single :math:`\vec{I}_{obs}`, a single
set of fitting parameters, and a single fit result. To store the multiple `lmfit.Parameter` objects,
`~dkist_processing_pac.fitter.fitter_parameters.PolcalDresserParameters` uses the custom `~dkist_processing_pac.fitter.fitter_parameters.NdParameterArray`.

Fitter
******

The `~dkist_processing_pac.fitter.polcal_fitter.PolcalFitter` is the main interface between `dkist-processing-pac` and
instrument pipelines. It ingests two `~dkist_processing_pac.input_data.dresser.Dresser` objects prepared by the instrument
(:ref:`one each for global and local fits <bins_and_fits>`) and uses them to initialize two
`~dkist_processing_pac.polcal_fitter.FitObjects` objects. These objects use their respective `~dkist_processing_pac.input_data.dresser.Dresser`
to initialize `~dkist_processing_pac.optics.telescope.Telescope`, `~dkist_processing_pac.optics.calibration_unit.CalibrationUnit`,
and `~dkist_processing_pac.fitter.fitter_parameters.PolcalDresserParameters`.

The `~dkist_processing_pac.fitter.polcal_fitter.PolcalFitter` then uses the global `~dkist_processing_pac.polcal_fitter.FitObjects`
to compute the best-fit Calibration Unit parameters. It then fixes these parameters in the local
`~dkist_processing_pac.polcal_fitter.FitObjects` and finally fits a modulation matrix for each :math:`\vec{I}_{obs}` in
the local Dresser.

Tying It All Together
---------------------

#. The instrument processes the PolCal files in whatever way is needed. These processed files are then organized into two
   dictionaries with type ``Dict[int, List[FitsAccess]]``. The key is the CS step number and the value is a list of
   `FitsAccess` objects, each one corresponding to a single modulator state. One dictionary contains data with only a
   single bin (presumably averaged over a large area); these are the "global" data. The second dictionary contains data
   binned at the level required for computing demodulation matrices; these are the "local" data.
#. The instrument uses those dictionaries to construct two (global and local) `~dkist_processing_pac.input_data.dresser.Dresser` objects.
#. A `~dkist_processing_pac.fitter.polcal_fitter.PolcalFitter` is created with the two `~dkist_processing_pac.input_data.dresser.Dresser` objects and the “fit mode” and “init set” parameters taken from the input dataset document.
#. As part of its `__init__  <dkist_processing_pac.fitter.polcal_fitter.PolcalFitter>`, the `~dkist_processing_pac.fitter.polcal_fitter.PolcalFitter` initializes two `~dkist_processing_pac.polcal_fitter.FitObjects` objects, each of which do the following

   a. Use the `~dkist_processing_pac.input_data.dresser.Dresser` to initialize `~dkist_processing_pac.optics.telescope.Telescope` and `~dkist_processing_pac.optics.calibration_unit.CalibrationUnit` objects
   b. Use the `~dkist_processing_pac.input_data.dresser.Dresser`, fit mode, and init set parameters to load sensible starting values into a
      `~dkist_processing_pac.fitter.fitter_parameters.PolcalDresserParameters` object. This is where we set the “global” parameters for the :math:`\mathbf{C}` matrix.
   c. Use that loaded `~dkist_processing_pac.fitter.fitter_parameters.PolcalDresserParameters` object to populate the `~dkist_processing_pac.optics.telescope.Telescope` and `~dkist_processing_pac.optics.calibration_unit.CalibrationUnit` objects with
      the configuration parameters not provided directly by the `~dkist_processing_pac.input_data.dresser.Dresser`.

#. The `~dkist_processing_pac.fitter.polcal_fitter.PolcalFitter` uses the global `~dkist_processing_pac.polcal_fitter.FitObjects` object to compute the global CU fit parameters
#. The `~dkist_processing_pac.fitter.polcal_fitter.PolcalFitter` fixes the global CU parameters for all bins in the local `~dkist_processing_pac.polcal_fitter.FitObjects` object
#. For each bin in the local `~dkist_processing_pac.input_data.dresser.Dresser` the `~dkist_processing_pac.fitter.polcal_fitter.PolcalFitter` does the following

   a. Initialize the non-global parameters that are specific to that single bin's :math:`\vec{I}_{obs}`
   b. Run fit of :math:`\mathbf{O}`
   c. Save the results

#. Once all bins are fit the set of all demodulation matrices is available to the instrument pipeline via the
   `~dkist_processing_pac.fitter.polcal_fitter.PolcalFitter.demodulation_matrices` property.

