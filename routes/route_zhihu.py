from flask import (
    render_template,
    Blueprint,
    request,
    redirect,
    url_for,
)

import json
from utils import log
from bson.objectid import ObjectId
from routes.route_user import (
    login_required,
    current_user,
)
from models.question_answer import (
    Question,
    Answer,
    AnswerComment,
)


main = Blueprint('zhihu', __name__)

# 主页
@main.route("/")
def index():
    u = current_user()
    all_question = Question.all()
    return render_template("zhihu/index.html", user=u, questions=all_question)


# 提交问题的视图
@main.route("/question_submit_view", endpoint='question_submit_view')
@login_required
def question_submit_view():
    return render_template("zhihu/question_submit.html")


# 提交问题的逻辑
@main.route("/question_submit", endpoint='question_submit', methods=['POST'])
@login_required
def question_submit():
    form = request.form.to_dict()
    Question.new(form)
    return redirect(url_for('.index'))


# 问题的详情页
@main.route("/question_detail/<string:id>",
            endpoint='question_detail', methods=['GET'])
@login_required
def question_detail(id):
    u = current_user()
    # 找到对应的问题
    q = Question.find_one(_id=ObjectId(id))
    if q is None:
        return redirect(url_for('.index'))
    else:
        # 找到问题对应的所有回答
        all_answer = Answer.all(question_id=q._id)
        return render_template('zhihu/question_detail.html',
                               user=u,
                               question=q,
                               answers=all_answer,
                               )


# 提交回答的逻辑
@main.route("/api/answer_submit", endpoint='answer_submit', methods=['POST'])
@login_required
def answer_submit():
    form = request.json
    log('answer dict', form)
    ans = Answer.new(form)
    # 返回 json 格式的 answer
    return ans.json()

# 被点赞
@main.route("/api/click_agree", endpoint='click_agree', methods=['POST'])
@login_required
def click_agree():
    # json
    data = json.loads(request.json)
    # 找到对应的 answer
    ans = Answer.find_one(_id=ObjectId(data['_id']))
    log('ans', ans)

    resp = ''
    # 如果 answer 存在
    if ans is not None:
        ans.agree = ans.agree + 1
        ans.save()
        # 返回 json 对象
        resp = dict(
            agree=ans.agree,
            id=ans._id,
        )
        resp = json.dumps(resp)

    return resp


# 加载所有的回答
@main.route("/api/all_answer/<string:question_id>",
            endpoint='all_answer', methods=['GET'])
@login_required
def all_answer(question_id):
    all = Answer.all(question_id=question_id)
    # 格式化为 json 返回
    res = json.dumps([ans.json() for ans in all])
    return res


# 提交回答评论的逻辑
@main.route("/api/answer_comment_submit",
            endpoint='answer_comment_submit', methods=['POST'])
@login_required
def answer_comment_submit():
    form = request.json
    log('comment answer dict', form)
    ans = AnswerComment.new(form)
    # 返回 json 格式的 answer
    return ans.json()


# 加载评论的所有回答
@main.route("/api/all_answer_comment/<string:answer_id>",
            endpoint='all_answer_comment', methods=['GET'])
@login_required
def all_answer_comment(answer_id):
    all = AnswerComment.all(answer_id=answer_id)
    # 格式化为 json 返回
    res = json.dumps([ans.json() for ans in all])
    return res
