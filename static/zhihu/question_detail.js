var log = console.log.bind(console, new Date().toLocaleString())

var sel = function (name) {
    return document.querySelector(name)
}

// 向服务器发送点赞数据，data 需要是 json 格式
var apiClickAgree = function(data, callback) {
    var path = '/zhihu/api/click_agree'
    ajax('POST', path, data, callback)
}

// 绑定事件，点赞按钮
var bindClickAgree = function () {
    var ans_list = sel('.answer-list')
    ans_list.addEventListener('click', function (event) {
        var t = event.target
        if (t.classList.contains('answer-agree')) {
            // 获取回答id
            var answer_id = t.closest('.answer-item').id
            var data = {
                id: answer_id,
            }

            // json格式化
            data = JSON.stringify(data)
            log('hit agree', data)

            // 发送 AJAX 请求
            apiClickAgree(data, function(resp){
                // 回调函数，更新点赞数值的显示
                log('resp', resp)
                if (resp == '') {
                    return
                }

                resp = JSON.parse(resp)
                if (('id' in resp) && ('agree' in resp)) {
                    id = resp.id
                    // 定位回答
                    ans = document.getElementById(id);
                    // 定位点赞
                    agree = ans.querySelector('.answer-agree')
                    agree.innerText = resp.agree + '赞'
                }
            })
        }
    })
}

// 向服务器发送回答 api
var apiClickSubmitAnswer = function(data, callback) {
    var path = '/zhihu/api/answer_submit'
    ajax('POST', path, data, callback)
}

var answerTemplate = function(ans) {
    var template = `
    <div class="answer-item border border-light" id="${ans.id}">
        <!-- 个人介绍 -->
        <div class="row answer-item-row">
            <div class="col-md-auto">
            <img class='user-image' src="/uploads/${ans.image}"/>
            </div>
            <div class="col-md-auto">
                <div class=""><a href="/user/?id=${ans.user_id}">${ans.author}</a></div>
                <div class="font-weight-light person-intro">个人介绍</div>
            </div>
        </div>
        <!-- 多少人赞同了该回答 -->
        <div class="answer-item-row font-weight-light agree-intro">
            4人赞同了该回答
        </div>
        <!-- 回答内容 -->
        <div class="answer-item-row">
            ${ans.content}
        </div>
        <!-- 回答编辑时间 -->
        <div class="answer-item-row font-weight-light answer-time">
            该回答编辑于 xxx
        </div>
        <!-- 相关按钮 -->
        <div class="answer-item-row">
            <!-- 点赞 -->
            <button type="button" class="btn btn-sm btn-outline-primary answer-agree">
                ${ans.agree}赞
            </button>
            <button type="button"  class="link-answer-comment">
            x 条评论
            </button>
        </div>

    </div>
    `
    return template
}

// 从 quill Delta 转化为 HTML
function quillGetHTML(inputDelta) {
    // log('HTML input', inputDelta)
    var tempQuill=new Quill(document.createElement("div"));
    tempQuill.setContents(inputDelta);
    // log('HTML output', tempQuill.root.innerHTML)
    return tempQuill.root.innerHTML;
}

// 向服务器发送回答
var bindClickSubmitAnswer = function(quill) {
    var button = sel('#button-submit-answer')
    if (button == null)  {
        return
    }
    button.addEventListener('click', function (event) {
        // 获取回答id
        var question_id = sel('#question-id').value
        // 获取回答content，实际上是 quill Delta
        var content = quill.getContents();
        // json格式化
        var data = {
            question_id: question_id,
            content: content,
        }
        // data = JSON.stringify(data)

        log('hit submit', data)
        // 发送 AJAX 请求
        apiClickSubmitAnswer(data, function(resp) {

            resp = JSON.parse(resp)
            // log('resp.content', resp.content)
            resp.content = JSON.parse(resp.content)
            // 将 Delta 转化为 HTML
            resp.content = quillGetHTML(resp.content)

            // 生成 HTML
            html = answerTemplate(resp)
            // 定位 answer-list
            var ans_list = sel('.answer-list')
            // 插入 before end
            ans_list.insertAdjacentHTML('beforeend', html)
            // 清空 quill 编辑器
            quill.setText('')
        })

    })
}

var init_editor = function () {
    // Initialize Quill editor
    var options = {
        placeholder: '我来回答 ...',
        theme: 'snow'
    };
    log('init editor')
    var div_editor = document.querySelector('#editor')
    if (div_editor == null) {
        log('editor null')
        return
    }
    var quill = new Quill('#editor', options);
    return quill
}

// 加载所有的回答
var loadAllAnswer = function () {
    // 获取回答id
    var question_id = sel('#question-id').value
    var path = '/zhihu/api/all_answer/' + question_id

    ajax('GET', path, {}, function(resp) {

        var ans_list = sel('.answer-list')
        // 解析 json
        all_answer = JSON.parse(resp)
        // log('all_answer', all_answer)
        // 用一个循环渲染 answer
        for (var ans of all_answer) {
            // log('ans before parse', ans)
            // 不懂为什么这里需要再parse一次
            ans.content = JSON.parse(ans.content)
            // log('ans', ans)
            // 将 Delta 转化为 HTML
            ans.content = quillGetHTML(ans.content)

            // 生成 HTML
            html = answerTemplate(ans)
            // 定位 answer-list
            var ans_list = sel('.answer-list')
            // 插入 before end
            ans_list.insertAdjacentHTML('beforeend', html)
        }
    })
}

// 向服务器发送点赞回答id，data 需要是 json 格式
var apiClickAnswerComment = function(data, callback) {
    var path = '/zhihu/api/all_answer_comment/' + data.answer_id
    ajax('GET', path, data, callback)
}

// 绑定事件，显示问答评论
var bindClickAnswerComment = function () {
    var ans_list = sel('.answer-list')
    ans_list.addEventListener('click', function (event) {
        var t = event.target
        if (t.classList.contains('link-answer-comment')) {
            // 获取回答id
            var answer_item = t.closest('.answer-item')
            var answer_id = answer_item.id
            var data = {
                answer_id: answer_id,
            }

            log('show answer comment', data)
            // 定位 comment_list
            var div_comment = answer_item.querySelector('.div-answer-comment')

            // 如果 div_comment 不为空，则清空
            if (div_comment != undefined) {
                div_comment.remove()
                return

            // 如果 div_comment 为空，则插入
            } else {
                var template = `
                <div class='div-answer-comment'></div>
                `
                answer_item.insertAdjacentHTML('beforeend', template)
                div_comment = answer_item.querySelector('.div-answer-comment')
            }

            // 插入评论 list
            var template_list = `
            <div class='answer-comment-list'></div>
            `
            div_comment.insertAdjacentHTML('afterbegin', template_list)
            var comment_list = div_comment.querySelector('.answer-comment-list')
            log('加载评论')
            // 发送 AJAX 请求
            apiClickAnswerComment(data, function(resp){
                // 将评论插入到回答底部
                resp = JSON.parse(resp)
                log('回答的评论', resp)
                for (var ans of resp) {
                    ans = JSON.parse(ans)
                    // 格式化时间
                    var dt = new Date(ans.time * 1000)
                    var dt_str = dt.toDateString()
                    var template = `
                        <div class='answer-comment-item'>
                            <span>${ans.author}</span>
                            <span class='answer-comment-time'>${dt_str}</span>
                            <br>
                            <span>${ans.content}</span>


                        </div>
                    `
                    comment_list.insertAdjacentHTML('beforeend', template)
                }
                // 插入评论输入框与按钮
                var template = `
                    <div class='div-answer-comment-submit'>
                        <input type="text" id="answer-comment-id" value=${answer_id} hidden=True>
                        <input type="text"
                            id="answer-comment-content"
                            placeholder='写下你的评论...'>
                        <button type="button" id='button-submit-answer-comment'>发布</button>
                    </div>
                `
                comment_list.insertAdjacentHTML('afterend', template)
            })
        }
    })
}


// 向服务器发送新增的评论
var apiSubmitAnswerComment = function(data, callback) {
    var path = '/zhihu/api/answer_comment_submit'
    ajax('POST', path, data, callback)
}

// 针对回答发表评论
var bindClickSubmitAnswerComment = function () {
    var ans_list = sel('.answer-list')
    ans_list.addEventListener('click', function (event) {
        var t = event.target
        // log('t', t.id)
        if (t.id == 'button-submit-answer-comment') {
            // 获取回答id
            var answer_item = t.closest('.answer-item')
            var answer_id = answer_item.id
            // 获取回答content
            var comment_submit = t.closest('.div-answer-comment-submit')
            var comment_input = comment_submit.querySelector('#answer-comment-content')
            var content = comment_input.value

            // json格式化
            var data = {
                answer_id: answer_id,
                content: content,
            }
            log('发布的评论内容', data)

            // 发送 AJAX 请求
            apiSubmitAnswerComment(data, function(resp) {
                ans = JSON.parse(resp)
                log('显示新增的评论', ans)
                var comment_list = answer_item.querySelector('.answer-comment-list')
                // 格式化时间
                var dt = new Date(ans.time * 1000)
                var dt_str = dt.toTimeString()
                var template = `
                    <div class='answer-comment-item'>
                        ${ans.author}
                        ${ans.content}
                        ${dt_str}
                    </div>
                `
                comment_list.insertAdjacentHTML('beforeend', template)
                // 清空输入
                comment_input.value = ''
            })
        }
    })
}


var _main = function () {
    // 加载所有回答
    loadAllAnswer()
    // 加载编辑器
    quill = init_editor()
    // 点赞的按钮
    bindClickAgree()
    // 提交回答的按钮
    bindClickSubmitAnswer(quill)
    // 显示问答的评论
    bindClickAnswerComment()
    // 针对回答发表评论
    bindClickSubmitAnswerComment()
}

_main()
