# Contributing Guidelines - *Datasets*

## Development Datasets

* Refers to all datasets that has been used for development.
* Datasets can be found by default on `app/data/*`.
* Development datasets must be properly labeled.
  * Dataset folder must be properly labeled, refering to the object type/classification
  * Dataset content (for recognition) must have `p` (passed) or `f` (failed) on the beginning of their file name.
  * Dataset content (for testing) must be seperated to either `*/passed/` or `*/failed/` folders with corresponding copies from the recognition dataset.
  * All dataset content labels should have a standardized number format appended, `xxx`, corresponding to their number in their respective classification and sub-classification.
  * Example:
  
  `app/data/facemask/p102.png`

  > a picture of a *passed* facemask numbered 102, has a copy at `app/data/facemask/passed/p102.png`.

## User-added Datasets

* Refers to all datasets (including altered) that has been added by the user.
* This includes, by definition, development datasets, if the user opts to save image captures as dataset.
* This also follows all conventions from the development dataset.
* Dataset contents are not to be retrieved in any form or way.
* Dataset contents can be expunged, when opted by the user.
* Development dataset contents can be excluded from the deletion when opted.
* Dataset can be used to retrain the system AI when opted by the user, given the danger notification.
