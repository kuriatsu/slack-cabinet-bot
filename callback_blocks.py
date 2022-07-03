#! /usr/bin/python3
# -*- coding: utf-8 -*-

def one_file_blocks(user_name, date):
    block = [
        {
        "type": "input",
        "block_id" : "document_type",
        "element": {
            "type": "static_select",
            "action_id": "event_type-action",
            "initial_option": {
                "text": {
                    "type": "plain_text",
                    "text": "Seminar Presentation",
                    "emoji": True
                },
                "value": "seminar_presentation"
            },
            "options": [
                {
                    "text": {
                        "type": "plain_text",
                        "text": "Seminar Presentation",
                        "emoji": True
                    },
                    "value": "seminar_presentation"
                },
                {
                    "text": {
                        "type": "plain_text",
                        "text": "Seminar Handout",
                        "emoji": True
                    },
                    "value": "seminar_handout"
                },
                {
                    "text": {
                        "type": "plain_text",
                        "text": "Rinko Textbook",
                        "emoji": True
                    },
                    "value": "rinko_textbook"
                },
                {
                    "text": {
                        "type": "plain_text",
                        "text": "Rinko Presentation",
                        "emoji": True
                    },
                    "value": "rinko_presentation"
                },
                {
                    "text": {
                        "type": "plain_text",
                        "text": "Rinko Excercise",
                        "emoji": True
                    },
                    "value": "rinko_ex"
                },
                {
                    "text": {
                        "type": "plain_text",
                        "text": "Paper Introduction",
                        "emoji": True
                    },
                    "value": "paper_intro"
                }
            ]
        },
        "label": {
            "type": "plain_text",
            "text": "Type",
            "emoji": True
        }
        },
        {
            "type": "input",
            "block_id" : "title",
            "element": {
                "type": "plain_text_input",
                "action_id": "title-action",
            },
            "label": {
                "type": "plain_text",
                "text": "Title",
                "emoji": True
            }
        },
        {
            "type": "input",
            "block_id" : "author",
            "element": {
                "type": "plain_text_input",
                "action_id": "author-action",
                "initial_value": user_name,
            },
            "label": {
                "type": "plain_text",
                "text": "Author",
                "emoji": True
            }
        },
        {
            "type": "input",
            "block_id" : "date",
            "element": {
                "type": "datepicker",
                "action_id": "date-action",
                "initial_date": str(date),
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select a date",
                    "emoji": True
                },
            },
            "label": {
                "type": "plain_text",
                "text": "Date",
                "emoji": True
            }
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "emoji": True,
                        "text": "Approve"
                    },
                    "style": "primary",
                    "value": "approve",
                    "action_id": "approve_action",
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "emoji": True,
                        "text": "Deny"
                    },
                    "style": "danger",
                    "value": "deny",
                    "action_id": "deny_action"
                }
            ]
        }
    ]
    return block

def two_file_blocks(user_name, date, file_names):
    block = [
    {
        "type": "input",
        "block_id" : "title",
        "element": {
            "type": "plain_text_input",
            "action_id": "title-action",
        },
        "label": {
            "type": "plain_text",
            "text": "Title",
            "emoji": True
        }
    },
    {
        "type": "input",
        "block_id" : "author",
        "element": {
            "type": "plain_text_input",
            "action_id": "author-action",
            "initial_value": user_name,
        },
        "label": {
            "type": "plain_text",
            "text": "Author",
            "emoji": True
        }
    },
    {
        "type": "input",
        "block_id" : "date",
        "element": {
            "type": "datepicker",
            "action_id": "date-action",
            "initial_date": str(date),
            "placeholder": {
                "type": "plain_text",
                "text": "Select a date",
                "emoji": True
            },
        },
        "label": {
            "type": "plain_text",
            "text": "Date",
            "emoji": True
        }
    }]

    for file_name in file_names:
        file_type_block = {
            "type": "input",
            "block_id" : f"document_type_{file_name}",
            "element": {
                "type": "static_select",
                "action_id": "document_type-action",
                "initial_option": {
                    "text": {
                        "type": "plain_text",
                        "text": "Seminar Presentation",
                        "emoji": True
                    },
                    "value": "seminar_presentation"
                },
                "options": [
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Seminar Presentation",
                            "emoji": True
                        },
                        "value": "seminar_presentation"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Seminar Handout",
                            "emoji": True
                        },
                        "value": "seminar_handout"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Rinko Textbook",
                            "emoji": True
                        },
                        "value": "rinko_textbook"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Rinko Presentation",
                            "emoji": True
                        },
                        "value": "rinko_presentation"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Rinko Excercise",
                            "emoji": True
                        },
                        "value": "rinko_ex"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Paper Introduction",
                            "emoji": True
                        },
                        "value": "paper_intro"
                    }
                ]
            },
            "label": {
                "type": "plain_text",
                "text": file_name,
                "emoji": True
            }
        }
        block.append(file_type_block)

    button_block = {
        "type": "actions",
        "elements": [
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "emoji": True,
                    "text": "Approve"
                },
                "style": "primary",
                "value": "approve",
                "action_id": "approve_action",
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "emoji": True,
                    "text": "Deny"
                },
                "style": "danger",
                "value": "deny",
                "action_id": "deny_action"
            }
        ]
    }
    block.append(button_block)

    return block
