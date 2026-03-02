from openai import OpenAI
from typing import Dict, Optional
from database import db_manager
from ai.scoring_anketas_system import anketa1_scores, anketa2_scores, anketa3_scores


class AnketAnalyzer:
    def __init__(self, openai_api_key: str):
        self.client = OpenAI(api_key=openai_api_key, base_url="https://api.aitunnel.ru/v1/")
        self._init_scoring_system()

    def _init_scoring_system(self):
        self.anketa1_scores = anketa1_scores
        self.anketa2_scores = anketa2_scores
        self.anketa3_scores = anketa3_scores


    def _calculate_section_score(self, data: Dict, scores: Dict) -> int:
        if not data:
            return 0
        total = 0
        for question, answer in data.items():
            if question in scores:
                score_config = scores[question]
                if isinstance(score_config, dict):
                    for key, value in score_config.items():
                        if key.lower() in answer.lower():
                            total += value
                            break
                elif isinstance(score_config, dict) and "max" in score_config:
                    if score_config["type"] == "count_3":
                        items = [x for x in answer.replace(",", " ").split() if len(x) > 2]
                        count = len(items)
                        total += min(3, count)
                    elif score_config["type"] == "sentences":
                        sentences = answer.count(".") + answer.count("!") + answer.count("?")
                        total += min(3, sentences)
                    elif score_config["type"] == "groups":
                        groups = [x for x in answer.split("/") if x.strip()]
                        count = len(groups)
                        if count >= 5:
                            total += 3
                        elif count >= 3:
                            total += 2
                        elif count >= 1:
                            total += 1
        return total

    async def analyze_peer_anketas(self, peer_id: int) -> Optional[str]:
        try:
            anketa0_data = await db_manager.get_anketa_data(peer_id, "anketa0")
            anketa1_data = await db_manager.get_anketa_data(peer_id, "anketa1")
            anketa2_data = await db_manager.get_anketa_data(peer_id, "anketa2")
            anketa3_data = await db_manager.get_anketa_data(peer_id, "anketa3")

            if not any([anketa0_data, anketa1_data, anketa2_data, anketa3_data]):
                return "❌ Заполните хотя бы одну анкету для анализа."

            section1_score = self._calculate_section_score(anketa1_data, self.anketa1_scores)
            section2_score = self._calculate_section_score(anketa2_data, self.anketa2_scores)
            section3_score = self._calculate_section_score(anketa3_data, self.anketa3_scores)

            prompt = self._build_prompt({
                "Раздел 1. Персональные данные": anketa0_data,
                "Раздел 2. Профессиональное самоопределение": anketa1_data,
                "Раздел 3. Мечта и путь к ней": anketa2_data,
                "Раздел 4. Модель героя-созидателя": anketa3_data
            }, section1_score, section2_score, section3_score)

            response = await self._get_ai_analysis(prompt)
            return response

        except Exception as e:
            return f"❌ Ошибка анализа: {str(e)}"

    def _build_prompt(self, anketas_data: Dict, s1_score: int, s2_score: int, s3_score: int) -> str:
        prompt_parts = ["📋 АНКЕТА ПРОФОРИЕНТАЦИИ\n\n"]

        for section_name, data in anketas_data.items():
            if data:
                prompt_parts.append(f"📂 {section_name}")
                prompt_parts.append("=" * 50)

                for question, answer in data.items():
                    prompt_parts.append(f"❓ {question}")
                    prompt_parts.append(f"💬 {answer}")
                    prompt_parts.append("")

                prompt_parts.append("")

        full_data = "\n".join(prompt_parts)

        analysis_prompt = f"""{full_data}

🤖 РАССЧИТАННЫЕ БАЛЛЫ:
Раздел 2: {s1_score}/32
Раздел 3: {s2_score}/23
Раздел 4: {s3_score}/33

ЗАДАЧА: Используя рассчитанные баллы, дай интерпретацию по этим диапазонам (СЛОВО В СЛОВО):

Раздел 2 (макс 32 балла):
• 25-32: "Ты очень уверенный, понимающий свой путь к реализации человек. Скорее всего ты уже знаешь себя и мир профессий достаточно, чтобы сделать осознанный выбор. Поэтому я могу только пожелать тебе реализовать все свои таланты."
• 20-24: "Ты достаточно хорошо понимаешь свои сильные стороны и уже выбрал направление развития. Советую тебе обсудить свой выбор с вдохновителями, которые уже реализовались в выбранной тобой сфере. Расспроси их о том, какие шаги лучше сделать в первую очередь и получи контакты полезных людей."
• 10-19: "У тебя есть сомнения. И это нормально. Даже хорошо. Потому что это значит, что ты думаешь и ищешь лучшее приложение для своих талантов. Наш тренинг «Путь к самореализации» идеально подойдет тебе для того, чтобы лучше понять свои стремления, увидеть свою силу и выявить лучший путь применения твоих талантов."
• 0-9: "Дружище, кажется ты в тупике. Возможно тебе неинтересно узнать себя лучше или же что-то тебе мешает. Хотим тебе помочь. Обязательно подойди к тренерам и вдохновтелям и поговори по душам. А еще я очень советую тебе отправиться на тренинг «Путь к самореализации». Он поможет тебе исследовать свои интересы и способности, определить пути развития и реализации твоего потенциала, разобраться в том, что стоит у тебя на пути."

Раздел 3 (макс 23 балла):
• 17-23: "Ты хорошо понимаешь свои желания, у тебя есть стратегия, которая позволяет достигать их. Это хороший знак. Путь у тебя все получится!"
• 9-16: "Ты пока в поиске ответов. Это прекрасно! Значит ты думающий человек! Наш тренинг «Формула мечты» - это идеальная площадка для твоей глубокой работы с самим собой. Если ты любишь смотреть глубоко, если тебе интересно, откуда появляются твои желания и как научиться формулировать их и исполнять их так, чтобы это делало тебя счастливым, то записывайся на этот тренинг. Ты не только получишь полезные навыки, но и выстроишь четкую картину мира."
• 0-8: "Ты пока не чувствуешь себя уверенно в этой теме. Сам факт наличия мечты и формирования желаний для тебя еще не пройденный этап, а путь их реализации - вообще тебе неизвестен. Значит наш тренинг «Формула мечты» точно будет тебе полезен. Ты узнаешь все, что нужно знать о мечтах, о желаниях и о счастье, научишься слушать себя, определять свои желания так, чтобы они тебя вдохновляли и чтобы действительно приносили тебе счастье, научишься ставить цели и точно спланируешь все шаги, которые помогут тебе успешно реализовать задуманное."

Раздел 4 (макс 33 балла):
• 27-33: "Ты двигаешься вперед точь-в-точь по модели героя-созидателя. Это значит, что ты активно развиваешься и растешь, опираясь на все элементы модели. Более того, ты понимаешь значимость и смысл каждого элемента модели и это помогает тебе уверенно идти вперед. Это круто!"
• 20-26: "Продолжай! Не сбавляй обороты! Ты идешь в верном направлении. Советую тебе больше времени провести с вдохновителями, чтобы насытиться их опытом и состоянием. И выбирай тренинг по вкусу, чтобы с радостью и с пользой для себя провести время."
• 10-19: "Дорогой друг! Ты пока в самом начале своего пути самоисследования. Тебе будет полезно хорошенько разобраться в том, что делает человека успешным и самодостаточным, а затем пройти разнообразные практики саморазвития. Запишись на тренинг по модели героя-созидателя, и выйди на новый уровень самопонимания!"
• 0-9: "Вероятно, тебе не очень интересно исследовать самого себя. А ведь именно это помогает двигаться к мечтам, реализовывать желания и достигать целей. Тренинг по модели героя-созидателя поможет тебе лучше разобраться в том, какие значимые элементы позволяют личности достичь высот и прокачать свои навыки и личностные качества для того, чтобы твоя личность обрела внутренние опоры."

Формат ответа:
**Раздел 2: {s1_score}/32 баллов**
[точный текст по баллам]

**Раздел 3: {s2_score}/23 баллов**
[точный текст по баллам]

**Раздел 4: {s3_score}/33 баллов**
[точный текст по баллам]

**ИТОГОВАЯ РЕКОМЕНДАЦИЯ:**"""

        return analysis_prompt

    async def _get_ai_analysis(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Ты профориентолог. Используй ТОЛЬКО предоставленные баллы и выдавай СЛОВО В СЛОВО интерпретации по диапазонам баллов."
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=1200,
            temperature=0.2
        )

        return response.choices[0].message.content