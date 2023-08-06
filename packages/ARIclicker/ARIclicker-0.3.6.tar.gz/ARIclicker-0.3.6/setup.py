from setuptools import setup, find_packages
with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()
setup(
    name = 'ARIclicker',
    version = '0.3.6',
    maintainer='lin_zhe',
    keywords='AutoRandomIntervalClicker',
    description = 'AutoRandomIntervalClicker',
    long_description_content_type='text/markdown',
    long_description=long_description,
    license = 'MIT License',
    author = 'lin_zhe',
    author_email = '2081812728@qq.com',
    packages = find_packages(),
    include_package_data = True,
    python_requires='>=3.0',
    platforms = 'any',
    install_requires = [
        'pynput','pyautogui','keyboard'
    ],
)
