from setuptools import setup, find_packages

DESCRIPTION = 'ArtByCode'
LONG_DESCRIPTION = """
# Welcome to ArtByCode Family

## Description

This is a beginner-level Python project, in this project we utilizes the Turtle graphics library to draw images using the coordinates derived form an external docx file.

### Usage

- Just install the package `pip install ArtByCode`
- Import it to you project `import ArtByCode` 
- Now you are good to enjoy our artworks in our gallery

### Built with

- Turtle 


### Example

```
    from ArtByCode import abc

    like = 'lord_ganesh'

    abc.subscribe(like).follow()
```

### OUTPUT
<div align = "center">
   <img src = "https://github.com/Art-by-Code/Coordinates/assets/114793988/2addc356-8db9-4404-b0ad-2ce0755c3511">
</div>



### Troubleshooting

- If you find any problem, you can contact me on [Instagram](https://www.instagram.com/art_by_code?r=nametag)
- You can also find more of my artworks on my youtube channel(https://www.youtube.com/@artbycode)


### Acknowledgements

Thanks to all my followers & friends.❤

### See also

- [Please visit my Youtube](https://www.youtube.com/@artbycode)
- [Please visit my Instagram](https://www.instagram.com/art_by_code?r=nametag)

### Consider supporting me

- If you like our content, please do like, follow & subscribe to our YouTube channel (https://www.youtube.com/@artbycode) and Instagram (https://www.instagram.com/art_by_code?r=nametag).
- Thanks ❤
"""
# Setting up
setup(
    name="ArtByCode",
    version='0.0.4',
    author="Coder Artist",
    author_email="abc4artbycode@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['turtle==0.0.1', 'docx', 'python-docx','requests'],
    keywords=['python', 'sketch', 'drawing', 'animation',
              'code hub', 'pencil sketch', 'painting'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)