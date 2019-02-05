# Utility scripts for biological data

This repository contains scripts that the Bio Code Group wrote that
are used to automate general lab computational tasks.

The main purpose of this repository is to practice programming through
projects that provide useful utilities for biological data. While many
of these are written in other groups as well, it provides a good starting
point for new students to familiarize themselves with biological data
and using Python to solve problems or automate tasks.

## Getting Started

Sequencing File Conveter allows the user to swap the format of their nucleic acid sequencing file (allowed file types: .qseq, .fastq, or .sam). Please refer to the seqfileconverter usage diagram to view the current supported swaps. 

### Prerequisites

Utility scripts are written in Python3.

### Installing

These are standalone scripts and can just be copied & run with python. 

```
git clone https://github.com/biocodegroup/utility-scripts.git
```

### Running the tests

Tests have not yet been created for this repository.

### Usage

To run sequencing file converter:
```
python seqfileconverter -f <input file> -o <output file> -d <discard file> -m <metadata file> -t <file type> 
```

## Contributing

This is a beginner, educational repository for students learning Python or R to contribute to. We are a small group of students at CSU studying biology and learning code through hands-on activities, please contact a member through the webpage to ask about joining before you contribute to this repository. 

### Proposed ideas: 
* qSeq to/from SAM file converter (can be added as a module to seqfileconverter)
* demultiplex libraries

## Authors

* **Charlotte Cialek** - *Initial work on file converter* - [ccialek](https://github.com/ccialek)
* **Josh Svendsen** - *Initial work on file converter* - [jmsvendsen](https://github.com/jmsvendsen)
See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

