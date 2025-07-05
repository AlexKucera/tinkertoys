#!/usr/bin/env python3
# encoding: utf-8
"""
query_yes_no.py

Interactive user prompts for yes/no questions with defaults.

Created by Alexander Kucera on 2013-05-23.
Copyright (c) 2024 BabylonDreams. All rights reserved.
"""

import sys
from typing import Optional, Union


def query_yes_no(question: str, default: Optional[str] = "yes") -> bool:
    """Ask a yes/no question via input() and return their answer.

    Args:
        question: A string that is presented to the user
        default: The presumed answer if the user just hits <Enter>.
                Must be "yes" (the default), "no" or None (meaning
                an answer is required of the user)

    Returns:
        True for yes, False for no

    Raises:
        ValueError: If default is not "yes", "no", or None
        KeyboardInterrupt: If user cancels with Ctrl+C
    """
    valid = {
        "yes": True, "y": True, "ye": True,
        "no": False, "n": False
    }
    
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError(f"invalid default answer: '{default}'")

    while True:
        try:
            choice = input(question + prompt).lower().strip()
            
            if default is not None and choice == '':
                return valid[default]
            elif choice in valid:
                return valid[choice]
            else:
                print("Please respond with 'yes' or 'no' (or 'y' or 'n').")
        
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            raise
        except EOFError:
            # Handle EOF (e.g., when input is redirected)
            if default is not None:
                return valid[default]
            else:
                raise ValueError("EOF encountered and no default provided")


def query_choice(question: str, choices: list, default: Optional[Union[str, int]] = None,
                case_sensitive: bool = False) -> str:
    """Ask a multiple choice question and return the selected choice.

    Args:
        question: A string that is presented to the user
        choices: List of valid choices
        default: Default choice (can be string or index)
        case_sensitive: Whether choices are case sensitive

    Returns:
        The selected choice as a string

    Raises:
        ValueError: If default is invalid
        KeyboardInterrupt: If user cancels with Ctrl+C
    """
    if not choices:
        raise ValueError("choices list cannot be empty")
    
    # Normalize choices for comparison
    if case_sensitive:
        valid_choices = {choice: choice for choice in choices}
    else:
        valid_choices = {choice.lower(): choice for choice in choices}
    
    # Handle default
    default_choice = None
    if default is not None:
        if isinstance(default, int):
            if 0 <= default < len(choices):
                default_choice = choices[default]
            else:
                raise ValueError(f"default index {default} out of range")
        else:
            if case_sensitive:
                if default in choices:
                    default_choice = default
                else:
                    raise ValueError(f"default '{default}' not in choices")
            else:
                if default.lower() in valid_choices:
                    default_choice = valid_choices[default.lower()]
                else:
                    raise ValueError(f"default '{default}' not in choices")
    
    # Create prompt
    choice_list = ', '.join(choices)
    if default_choice:
        prompt = f" [{choice_list}] (default: {default_choice}) "
    else:
        prompt = f" [{choice_list}] "

    while True:
        try:
            choice = input(question + prompt).strip()
            
            if choice == '' and default_choice:
                return default_choice
            
            # Check if choice is valid
            check_choice = choice if case_sensitive else choice.lower()
            if check_choice in valid_choices:
                return valid_choices[check_choice]
            else:
                print(f"Please choose from: {choice_list}")
        
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            raise
        except EOFError:
            if default_choice:
                return default_choice
            else:
                raise ValueError("EOF encountered and no default provided")