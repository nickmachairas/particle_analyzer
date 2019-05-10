# from .context import particle_analyzer

from particle_analyzer.core import ParticleData


if __name__ == "__main__":
    # test1 = ParticleData('20180501_120357_001.xml')
    # print(test1.df.head())
    # print(test1.df.info())
    # print(test1.df.describe())
    # test1.show_image(0)
    # test2 = ParticleData('ottawa sand 2030.xml')
    # print(test2.df.head())
    # print(test2.df.info())
    # print(test2.df.describe())
    test3 = ParticleData('Silica 20-30 1.xml')
    # print(test3.df.head())
    # print(test3.df.info())
    # print(test3.df.EQPC.describe())
    test3.show_image(4888)
    # test4 = ParticleData('Peach river 1.xml')
    # print(test4.df.head())
    # print(test4.df.info())
    # print(test4.df.EQPC.describe())
    # test4.show_image(493)
