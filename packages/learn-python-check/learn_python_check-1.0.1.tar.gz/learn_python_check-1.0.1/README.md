 <img src="https://raw.githubusercontent.com/TUDelft-CITG/learn-python/main/book/figures/learn-python-logo.png" width=80/> 

# Learn Python for Civil Engineering and Geoscience check answers

A Python package for validating online course _Learn Python for Civil Engineering and Geosciences_ answers.

## Installation and updating
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the last stable version of the package. 

```bash
pip install learn-python-check
```

## Usage
The package allows for evaluating the answers to the exercises in sections 3, 4 and 6. 

#### Demo of some of the features:

```python
import learn_python_check.check_answers as check

check.notebook_3(question_number=0, arguments=[car_info, message])

```
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[GNU](https://choosealicense.com/licenses/gpl-3.0/)

## Acknowledgments

Financial support for this project was provided through an open education grant from the Educational Management Team for the Civil Engineering and Geosciences Faculty at Delft. The content was first developed for Summer 2022 by Sandra Verhagen and a team of TA's in Jupyter notebooks that were auto-graded in Vocareum. For Summer 2023 a second round of funding was optained to update the content and adapt it to an entirely open and self-paced course without enrollement via a Jupyter Book, led by Robert Lanzafame. Special thanks goes to Miguel Mendoza Lugo who adapted the notebooks into the Jupyter Book format and implemented the interactive features, as well as Ahmed Farahat, who helped create the fun new visual features that make understanding the material easier in the Jupyter Book platform, as well as the In a Nutshell summaries.

This Book is maintained and developed by staff of the Faculty of Civil Engineering and Geosciences of TU Delft, the Netherlands.

 <img src="https://raw.githubusercontent.com/TUDelft-CITG/learn-python/main/book/figures/TUDelft_logo_cmyk.png" width=170  style="float: right;"/> 
