from ttbot.server import Action, Post, Request, Server


class MyBot(Server):
    async def message_handler(self, post: Post) -> str:
        ''' Called when bot mentioned in post, return text will be published as reply post '''
        post.user_id    # int, who send post
        post.chat_id    # int, in what chat
        post.post_no    # int, post number
        post.text       # str, post text
        post.team_id    # int, if chat from team
        post.reply_no       # int, if post has reply to other post (number)
        post.reply_text     # str, if post has reply to other post (text)
        return f'Received {post}'

    async def action_handler(self, action: Action) -> dict:
        ''' Called when user clicks on bot action link or button '''
        action.action   # str, action name
        action.params   # dict, params of action
        action.post             # Post, post which attached action
        action.post.user_id     # int, who send post
        action.post.chat_id     # int, in what chat
        action.post.post_no     # int, post number
        action.post.text        # str, post text
        action.post.team_id     # int, if chat from team
        return {'action': str(action)}

    async def api_handler(self, request: Request) -> dict:
        ''' Web server for bot local aims '''
        request.method      # str, HTTP method
        request.path        # str, HTTP path
        request.query       # dict, parsed HTTP url query string
        request.headers     # dict, parsed HTTP headers
        request.data        # dict, parsed json from HTTP body
        return {'request': str(request)}


app = MyBot()
