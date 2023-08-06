# MyPackage

## MyPackage is a Python package that provides a simple NLP pipeline using spaCy.

# Installation

## Clone the repository and navigate to the root directory. Then run the following command:
    pip install NLPSimplified
    pip install spacy
    spacy download en_core_web_sm

## Here's some example code:
    from NLPSimplified import NlpPipeline, tokenize, pos_tagging, named_entity_recognition

    def main():
        # Create an instance of NlpPipeline
        pipeline = NlpPipeline()

        # Add the functions to the pipeline
        pipeline.add_to_pipeline(tokenize)
        pipeline.add_to_pipeline(pos_tagging)
        pipeline.add_to_pipeline(named_entity_recognition)

        # Sample text
        text = "OpenAI is a research organization located in San Francisco."

        # Process the text through the pipeline
        doc = pipeline.process(text)

        # Print the results
        print("Tokens:", doc._.tokens)
        print("POS tags:", doc._.pos_tags)
        print("Named entities:", doc._.entities)

    if __name__ == "__main__":
        main()

## Thanks to the spaCy team for developing the spaCy module, which forms the basis of this module!!

# Contributions

## Contributions can be made at the official GitHub page at : https://github.com/RedMythic1/NLPSimplified/

# License

## Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

## The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

## **THE SOFTWARE IS PROVIDED “AS IS”, _WITHOUT WARRANTY_ OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.**

# Contact
## Contact me at avnehb@gmail.com