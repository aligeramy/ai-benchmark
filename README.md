# LLM Physics Programming Benchmark

## Overview
This repository contains a standardized benchmark for evaluating Large Language Models' (LLMs) capabilities in physics-based programming tasks. The benchmark focuses on testing the models' ability to understand and implement complex physics simulations, geometric calculations, and real-time graphics programming.

## The Challenge
Each LLM is given the following prompt:

> Write a Python program that shows a ball bouncing inside a spinning hexagon. The ball should be affected by gravity and friction, and it must bounce off the rotating walls realistically.

This challenge tests multiple capabilities:
- Physics simulation (gravity, friction, collision detection)
- Geometric calculations (rotating hexagon, bounce angles)
- Real-time graphics programming
- Code organization and clarity
- Performance optimization

## Evaluation Criteria
LLMs are evaluated based on:
1. **Correctness**: Does the simulation follow proper physics laws?
2. **Completeness**: Are all requirements implemented?
3. **Code Quality**: Is the code well-structured and documented?
4. **Performance**: Does the simulation run smoothly?
5. **Error Handling**: Does the program handle edge cases?

## Results

### Models Tested
The following models have been tested on this benchmark:

1. **Claude 3.5 Sonnet (3.5)** - `sonnet-35.py`
2. **Claude 3.7 Sonnet (3.7)** - `sonnet-37.py`
3. **Claude 3.7 Sonnet Thinking (3.7)** - `sonnet-37-thinking.py`
4. **OpenAI GPT-o1** - `o1.py`

## Contributing
Feel free to contribute by testing new LLMs and submitting their results. Please follow the standard testing procedure and document your findings.


