from fastapi import FastAPI, HTTPException
import uvicorn
import openai

app = FastAPI()

# 设置你的OpenAI GPT-3.5 API密钥
OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY


@app.post("/generate-answer/")
def generate_answer(data: dict):
    question_type = data.get("question_type")
    question = data.get("question")
    options = data.get("options")

    if not question_type or not question or not options:
        raise HTTPException(status_code=400, detail="Missing required fields")

    system = '''我将给你一个题目，你需要解析这个题目并给出答案和解题思路
我将会给你三种题型【单选题、多选题、判断题】，
你需要分析题目的题面，单选题只能选择一个答案，多选题需要选择所有满足条件的答案，判断题需要判断题面描述内容是不是正确的
下面是例子1：
{
    "question_type": "多选题",
    "question": "关于脊柱结核脓肿错误的是",
    "options": [
    "A.脊椎结核脓肿的主要特征是常经筋膜间隙流注",
    "B.寒性脓肿的主要表现有椎旁脓肿和流注脓肿",
    "C.单纯寒性脓肿处理首先考虑抽脓并注入抗结核药",
    "D.寒性脓肿穿刺进针部位于脓肿表面皮肤处进针",
    "E.可于脓肿低位穿刺抽脓，一旦形成窦道便于引流"
    }
你的输出：
{"解题思路":"1.题目是多选题，我需要选择所有满足条件的答案
              2.题面需要判断哪些是错误的，我需要找出错误的结论
			  3.选项A 结论错误，符合题面
			    选项B 结论错误，符合题面
				选项C 结论错误，符合题面
			    选项D 结论错误，符合题面
				选项E 结论正确，不符合题面",
 "answer":	"[A,B,C,D]"
} 
例子2：
{
    "question_type": "多选题",
    "question": "三角肌止点以上的肱骨十骨折，骨折近侧段受哪些牵托？",
    "options": [
            "A.肱三头肌",
            "B.三角肌",
            "C.胸大肌",
            "D.背阔肌",
            "E.大网肌"
        ]
}
你的输出：
{"解题思路":"1.题目是多选题，我需要选择所有满足条件的答案
              2.题面需要判断哪些是正确的，我需要找出正确的结论
			  3.选项A 结论错误，不符合题面
			    选项B 结论错误，不符合题面
				选项C 结论正确，符合题面
			    选项D 结论正确，符合题面
				选项E 结论正确，符合题面",
 "answer":	"[C,D,E]"
} '''

    query = f"Question Type: {question_type}" \
            f"Question: {question}" \
            f"Options: {', '.join(options)}"
    print(query)

    prompts = [
        {'role': 'system', 'content': system},
        {'role': 'user', 'content': query},
    ]

    completion = openai.ChatCompletion.create(
        temperature=0.7,
        model="gpt-3.5-turbo",
        messages=prompts,
    )
    return {
        "answer": completion.choices[0].message.content,
    }


if __name__ == '__main__':
    uvicorn.run(app,host='10.99.7.67',port=8000)
