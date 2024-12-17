import asyncio
import logging
import os
import random
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from gtts import gTTS
from googletrans import Translator
from config import TOKEN


