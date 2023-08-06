# mACHINE LEARNING SETUP FILE
from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.1.2'
DESCRIPTION = '''

        The Regression class simplifies regression analysis by providing a convenient and flexible approach for model training, evaluation, and hyperparameter tuning.The Classifier class streamlines classification tasks by offering a well-organized framework for model selection, hyperparameter tuning, 
        and performance evaluation with diverse classifiers.

'''
LONG_DESCRIPTION = '''
        The Regression class provides a convenient and flexible way to perform regression analysis in Python, allowing for easy model training, evaluation, and hyperparameter tuning. By encapsulating various regression algorithms and metrics, it simplifies the process of building and comparing regression models, ultimately aiding in accurate predictions and insights.The "Classifier" class provides a convenient and organized way to perform various machine learning classification tasks, including model selection, hyperparameter tuning, and performance evaluation, with a wide range of classifiers. It encapsulates common functionality and enables easy comparison of multiple classifiers, making it a useful tool for classification tasks.'''

# Setting up
setup(
    name="AlgoMaster",
    version=VERSION,
    author="sajo sam",
    author_email="<sajosamambalakara@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['pandas', 'numpy', 'sklearn', 'xgboost', 'scikit-learn'],
    keywords=['machine learning', 'classifiers', 'logistic regression', 'k-nearest neighbors', 'naive Bayes', 'random forests', 'support vector machines', 
              'ensemble methods', 'hyperparameter tuning','performance evaluation', 'comparison', 'multiple classifiers'
              'advantages', 'Regression class', 'regression analysis, Python', 'model training', 'evaluation', 'hyperparameter tuning', 'encapsulating', 'regression algorithms', 
              'metrics', 'simplifies', 'building', 'comparing', 'regression models', 'accurate predictions', 'insights'
              ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

