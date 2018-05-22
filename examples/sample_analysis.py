# from .context import particle_analyzer

from particle_analyzer.core import ParticleData


if __name__ == "__main__":
    test1 = ParticleData('20180501_120357_001.xml')
    print(test1.df.head())
    print(test1.df.info())
    print(test1.df.describe())
    test2 = ParticleData('ottawa sand 2030.xml')
    print(test2.df.head())
    print(test2.df.info())
    print(test2.df.describe())
