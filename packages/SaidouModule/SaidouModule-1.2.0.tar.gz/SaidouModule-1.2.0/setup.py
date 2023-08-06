from setuptools import setup

setup(
    name='SaidouModule',
    version='1.2.0',
    author='Meddahi Saïd',
    author_email='s.meddahi.fo@gmail.com',
    description='Module possédant plusieurs packages, lire le README.md pour plus d\'informations.',
    long_description='Se module possède 2 sous-modules :\n\t-SaidouNeurones, qui possède deux script permettant d\'implémenter un réseau de neurones à couches cachés.\n\t-SaidouPixels, possède un script \'Pixels.py\' qui permet de créer, générer et charger des images possédant des pixels à \'n\' couches (3 pour les vecteurs couleurs RGB) avec des valeurs de pixels aléatoires enter 0 et 255.\n\n Pour installer se module suffit d\'ouvrir un terminal et de taper la commande `pip install SaidouModules`, ensuite dans votre script Python vous pouvez importé les différents packages.\n\tPar exemple pour SaidouPixels ajoutez cette ligne : `import SaidouPixels.Pixels as sp`.\n\tPour SaidouNeurones : `import SaidouNeurones.ReseauNeuronesSaid as rns` - `import SaidouNeurones.SaidouNeuroneV2 as snv2`.\n\n Se modules sera amener à être optimiser et évoluer.',
    url='https://github.com/SMedd69/SaidouModule',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    packages=['SaidouPixels', 'SaidouNeurones'],
    install_requires=['numpy',
                      'matplotlib',
                      'opencv-python',
                      'tqdm',
                      'scikit-learn'
                      ])
