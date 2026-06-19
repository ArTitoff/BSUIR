import time
import matplotlib.pyplot as plt
import spacy

# Загружаем модель
nlp = spacy.load("en_core_web_md")

# Тексты разной длины
texts = [
    "The cat sleeps.",  # короткий
    "The quick brown fox jumps over the lazy dog.",  # средний
    "Natural language processing helps computers understand human language. It is used in chatbots and translators.",
    """Natural language processing helps machines understand human communication.
            Computer vision allows machines to see and interpret images.
            Robotics combines AI with physical machines to automate tasks.
            The future of AI holds both promise and challenges for society.""",
            """"Natural language processing helps machines understand human communication.
            Computer vision allows machines to see and interpret images.
            Robotics combines AI with physical machines to automate tasks.
            The future of AI holds both promise and challenges for society.Natural language processing helps machines understand human communication.
            Computer vision allows machines to see and interpret images.
            Robotics combines AI with physical machines to automate tasks.
            The future of AI holds both promise and challenges for society.""",
      """Machine learning algorithms analyze text data. They find patterns and make predictions. Deep learning models are very effective for this task. Training requires a lot of data and time. Artificial intelligence is changing the world. AI helps in medicine, finance, and education. Scientists develop new algorithms every day. The future of AI is exciting. Many companies invest in AI research. Neural networks can now generate text and images. This technology will continue to improve. 
            Artificial intelligence is transforming the world in many ways.
            From healthcare to finance, AI systems are making decisions.
            Natural language processing helps machines understand human communication.
            Computer vision allows machines to see and interpret images.
            Robotics combines AI with physical machines to automate tasks.
            The future of AI holds both promise and challenges for society.""",  # длиннее
    """Machine learning algorithms analyze text data. They find patterns and make predictions. Deep learning models are very effective for this task. Training requires a lot of data and time. Artificial intelligence is changing the world. AI helps in medicine, finance, and education. Scientists develop new algorithms every day. The future of AI is exciting. Many companies invest in AI research. Neural networks can now generate text and images. This technology will continue to improve. 
            Artificial intelligence is transforming the world in many ways.
            From healthcare to finance, AI systems are making decisions.
            Natural language processing helps machines understand human communication.
            Computer vision allows machines to see and interpret images.
            Robotics combines AI with physical machines to automate tasks.
            The future of AI holds both promise and challenges for society.
            Researchers continue to develop new algorithms and applications.
            Ethical considerations are important in AI development.
            The field evolves rapidly with new breakthroughs each year.
            Education and training are essential for AI workforce development.""" ,
                         """The cat sleeps on the mat.
            
           The quick brown fox jumps over the lazy dog. 
            The sun is shining brightly in the blue sky. 
            Birds are singing in the green forest.
            
           Natural language processing is a field of artificial intelligence.
            It helps computers understand human language. 
            Many applications use NLP including translators and chatbots.
            The technology continues to improve every year.
            Machine learning algorithms can process large amounts of text data.
            They identify patterns and learn from examples. 
            Deep learning models are particularly effective for language tasks.
            These models use neural networks with many layers.
            Training requires significant computational resources and time.  
            
            Artificial intelligence is transforming the world in many ways.
            From healthcare to finance, AI systems are making decisions.
            Natural language processing helps machines understand human communication.
            Computer vision allows machines to see and interpret images.
            Robotics combines AI with physical machines to automate tasks.
            The future of AI holds both promise and challenges for society.
            Researchers continue to develop new algorithms and applications.
            Ethical considerations are important in AI development.
            The field evolves rapidly with new breakthroughs each year.
            Education and training are essential for AI workforce development.""" # самый длинный
]

word_counts = []
processing_times = []

print("Анализ текстов...")
print("-" * 40)

for i, text in enumerate(texts, 1):
    # Считаем слова в тексте
    words = len(text.split())
    
    # Замеряем время
    start = time.time()
    doc = nlp(text)
    elapsed = time.time() - start
    
    # Сохраняем данные
    word_counts.append(words)
    processing_times.append(elapsed)
    
    print(f"Текст {i}: {words} слов -> {elapsed:.3f} сек")

# Строим график
plt.figure(figsize=(8, 5))
plt.plot(word_counts, processing_times, 'bo-', linewidth=2, markersize=8)
plt.title('Время обработки от количества слов')
plt.xlabel('Количество слов')
plt.ylabel('Время (секунды)')
plt.grid(True)
plt.tight_layout()
plt.show()

print("\nГотово!")