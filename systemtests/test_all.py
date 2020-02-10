import pytest_bdd

from fixtures import *
from features.steps.givens import *
from features.steps.whens import *
from features.steps.thens import *

pytest_bdd.scenarios('features')
