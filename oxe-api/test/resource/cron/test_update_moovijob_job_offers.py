import os
from unittest.mock import patch, Mock

from test.BaseCase import BaseCase


class TestUpdateMoovijobJobOffers(BaseCase):

    @BaseCase.login
    @BaseCase.grant_access("/cron/update_moovijob_job_offers")
    @patch('utils.request.request.urlopen')
    def test_ok(self, mock_urlopen, token):
        self.db.insert({"id": 1, "name": "Moovijob"}, self.db.tables["Company"])

        a = Mock()
        a.read.side_effect = [
            open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "data", "page 1 on 1.json"), "r",
                 encoding="utf8").read()
        ]
        mock_urlopen.return_value = a

        response = self.application.post('/cron/update_moovijob_job_offers',
                                         headers=self.get_standard_post_header(token))

        articles = self.db.get(self.db.tables["Article"])
        article_versions = self.db.get(self.db.tables["ArticleVersion"])
        article_boxes = self.db.get(self.db.tables["ArticleBox"])

        self.assertEqual(200, response.status_code)

        self.assertEqual(len(articles), 2)
        self.assertEqual(articles[0].id, 1)
        self.assertEqual(articles[0].type, "JOB OFFER")
        self.assertEqual(articles[0].status, "PUBLIC")
        self.assertEqual(articles[0].external_reference, "26870")
        self.assertEqual(articles[1].id, 2)
        self.assertEqual(articles[1].type, "JOB OFFER")
        self.assertEqual(articles[1].status, "PUBLIC")
        self.assertEqual(articles[1].external_reference, "8331")

        self.assertEqual(len(article_versions), 2)
        self.assertEqual(article_versions[0].article_id, 1)
        self.assertEqual(article_versions[0].name, "Generated by cron/update_moovijob_job_offers")
        self.assertEqual(article_versions[0].is_main, 1)
        self.assertEqual(article_versions[1].article_id, 2)
        self.assertEqual(article_versions[1].name, "Generated by cron/update_moovijob_job_offers")
        self.assertEqual(article_versions[1].is_main, 1)

        self.assertEqual(len(article_boxes), 2)
        self.assertEqual(article_boxes[0].article_version_id, 1)
        self.assertEqual(article_boxes[0].position, 1)
        self.assertEqual(article_boxes[0].type, "PARAGRAPH")
        self.assertEqual(article_boxes[0].content, "English body #1")
        self.assertEqual(article_boxes[1].article_version_id, 2)
        self.assertEqual(article_boxes[1].position, 1)
        self.assertEqual(article_boxes[1].type, "PARAGRAPH")
        self.assertEqual(article_boxes[1].content, "French Body #2")

    @BaseCase.login
    @BaseCase.grant_access("/cron/update_moovijob_job_offers")
    @patch('utils.request.request.urlopen')
    def test_ok_with_2_pages(self, mock_urlopen, token):
        self.db.insert({"id": 1, "name": "Moovijob"}, self.db.tables["Company"])

        a = Mock()
        a.read.side_effect = [
            open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "data", "page 1 on 2.json"), "r",
                 encoding="utf8").read(),
            open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "data", "page 2 on 2.json"), "r",
                 encoding="utf8").read()
        ]
        mock_urlopen.return_value = a

        response = self.application.post('/cron/update_moovijob_job_offers',
                                         headers=self.get_standard_post_header(token))

        articles = self.db.get(self.db.tables["Article"])
        article_versions = self.db.get(self.db.tables["ArticleVersion"])
        article_boxes = self.db.get(self.db.tables["ArticleBox"])

        self.assertEqual(200, response.status_code)
        self.assertEqual(len(articles), 4)
        self.assertEqual(len(article_versions), 4)
        self.assertEqual(len(article_boxes), 4)

    @BaseCase.login
    @BaseCase.grant_access("/cron/update_moovijob_job_offers")
    @patch('utils.request.request.urlopen')
    def test_ok_with_existing_articles(self, mock_urlopen, token):
        self.db.insert({"id": 1, "name": "Moovijob"}, self.db.tables["Company"])

        self.db.insert({"id": 1, "title": "TITLE", "external_reference": "26870", "type": "JOB OFFER",
                        "status": "PUBLIC"}, self.db.tables["Article"])
        self.db.insert({"id": 1, "article_id": 1, "name": "VERSION 0", "is_main": 1}, self.db.tables["ArticleVersion"])
        self.db.insert({"id": 1, "article_version_id": 1, "position": 1, "content": "Box content", "type": "PARAGRAPH"},
                       self.db.tables["ArticleBox"])

        self.db.insert({"id": 2, "title": "TITLE", "external_reference": "8331", "type": "JOB OFFER",
                        "status": "PUBLIC"}, self.db.tables["Article"])
        self.db.insert({"id": 2, "article_id": 2, "name": "VERSION 0", "is_main": 0}, self.db.tables["ArticleVersion"])
        self.db.insert({"id": 3, "article_id": 2, "name": "VERSION 1", "is_main": 1}, self.db.tables["ArticleVersion"])

        a = Mock()
        a.read.side_effect = [
            open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "data", "page 1 on 1.json"), "r",
                 encoding="utf8").read()
        ]
        mock_urlopen.return_value = a

        response = self.application.post('/cron/update_moovijob_job_offers',
                                         headers=self.get_standard_post_header(token))

        articles = self.db.get(self.db.tables["Article"])
        article_versions = self.db.get(self.db.tables["ArticleVersion"])
        article_boxes = self.db.get(self.db.tables["ArticleBox"])

        self.assertEqual(200, response.status_code)

        self.assertEqual(len(articles), 2)
        self.assertEqual(articles[0].id, 1)
        self.assertEqual(articles[0].type, "JOB OFFER")
        self.assertEqual(articles[0].status, "PUBLIC")
        self.assertEqual(articles[0].external_reference, "26870")
        self.assertEqual(articles[1].id, 2)
        self.assertEqual(articles[1].type, "JOB OFFER")
        self.assertEqual(articles[1].status, "PUBLIC")
        self.assertEqual(articles[1].external_reference, "8331")

        self.assertEqual(len(article_versions), 3)
        self.assertEqual(article_versions[0].article_id, 1)
        self.assertEqual(article_versions[0].name, "VERSION 0")
        self.assertEqual(article_versions[0].is_main, 1)
        self.assertEqual(article_versions[1].article_id, 2)
        self.assertEqual(article_versions[1].name, "VERSION 0")
        self.assertEqual(article_versions[1].is_main, 0)
        self.assertEqual(article_versions[2].article_id, 2)
        self.assertEqual(article_versions[2].name, "VERSION 1")
        self.assertEqual(article_versions[2].is_main, 1)

        self.assertEqual(len(article_boxes), 2)
        self.assertEqual(article_boxes[0].article_version_id, 1)
        self.assertEqual(article_boxes[0].position, 1)
        self.assertEqual(article_boxes[0].type, "PARAGRAPH")
        self.assertEqual(article_boxes[0].content, "English body #1")
        self.assertEqual(article_boxes[1].article_version_id, 3)
        self.assertEqual(article_boxes[1].position, 1)
        self.assertEqual(article_boxes[1].type, "PARAGRAPH")
        self.assertEqual(article_boxes[1].content, "French Body #2")

    @BaseCase.login
    @BaseCase.grant_access("/cron/update_moovijob_job_offers")
    @patch('utils.request.request.urlopen')
    def test_ok_with_existing_articles_2(self, mock_urlopen, token):
        self.db.insert({"id": 1, "name": "Moovijob"}, self.db.tables["Company"])

        self.db.insert({"id": 1, "title": "TITLE", "external_reference": "26870", "type": "JOB OFFER",
                        "status": "PUBLIC"}, self.db.tables["Article"])
        self.db.insert({"id": 1, "article_id": 1, "name": "VERSION 0", "is_main": 1}, self.db.tables["ArticleVersion"])
        self.db.insert({"id": 1, "article_version_id": 1, "position": 1, "content": "Box content", "type": "PARAGRAPH"},
                       self.db.tables["ArticleBox"])
        self.db.insert({"id": 2, "article_version_id": 1, "position": 2, "content": "Box content", "type": "TITLE1"},
                       self.db.tables["ArticleBox"])

        self.db.insert({"id": 2, "title": "TITLE", "external_reference": "8331", "type": "JOB OFFER",
                        "status": "PUBLIC"}, self.db.tables["Article"])
        self.db.insert({"id": 3, "article_id": 2, "name": "VERSION 1", "is_main": 1}, self.db.tables["ArticleVersion"])
        self.db.insert({"id": 3, "article_version_id": 3, "position": 1, "content": "French Body #2",
                        "type": "PARAGRAPH"}, self.db.tables["ArticleBox"])

        a = Mock()
        a.read.side_effect = [
            open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "data", "page 1 on 1.json"), "r",
                 encoding="utf8").read()
        ]
        mock_urlopen.return_value = a

        response = self.application.post('/cron/update_moovijob_job_offers',
                                         headers=self.get_standard_post_header(token))

        articles = self.db.get(self.db.tables["Article"])
        article_versions = self.db.get(self.db.tables["ArticleVersion"])
        article_boxes = self.db.get(self.db.tables["ArticleBox"])

        self.assertEqual(200, response.status_code)

        self.assertEqual(len(articles), 2)
        self.assertEqual(articles[0].id, 1)
        self.assertEqual(articles[0].type, "JOB OFFER")
        self.assertEqual(articles[0].status, "PUBLIC")
        self.assertEqual(articles[0].external_reference, "26870")
        self.assertEqual(articles[1].id, 2)
        self.assertEqual(articles[1].type, "JOB OFFER")
        self.assertEqual(articles[1].status, "PUBLIC")
        self.assertEqual(articles[1].external_reference, "8331")

        self.assertEqual(len(article_versions), 2)
        self.assertEqual(article_versions[0].article_id, 1)
        self.assertEqual(article_versions[0].name, "VERSION 0")
        self.assertEqual(article_versions[0].is_main, 1)
        self.assertEqual(article_versions[1].article_id, 2)
        self.assertEqual(article_versions[1].name, "VERSION 1")
        self.assertEqual(article_versions[1].is_main, 1)

        self.assertEqual(len(article_boxes), 3)
        self.assertEqual(article_boxes[0].article_version_id, 1)
        self.assertEqual(article_boxes[0].position, 1)
        self.assertEqual(article_boxes[0].type, "PARAGRAPH")
        self.assertEqual(article_boxes[0].content, "Box content")
        self.assertEqual(article_boxes[1].article_version_id, 1)
        self.assertEqual(article_boxes[1].position, 2)
        self.assertEqual(article_boxes[1].type, "TITLE1")
        self.assertEqual(article_boxes[1].content, "Box content")
        self.assertEqual(article_boxes[2].article_version_id, 3)
        self.assertEqual(article_boxes[2].position, 1)
        self.assertEqual(article_boxes[2].type, "PARAGRAPH")
        self.assertEqual(article_boxes[2].content, "French Body #2")

    @BaseCase.login
    @BaseCase.grant_access("/cron/update_moovijob_job_offers")
    @patch('utils.request.request.urlopen')
    def test_ko_no_article(self, mock_urlopen, token):
        self.db.insert({"id": 1, "name": "Moovijob"}, self.db.tables["Company"])

        a = Mock()
        a.read.side_effect = [
            "{}"
        ]
        mock_urlopen.return_value = a

        response = self.application.post('/cron/update_moovijob_job_offers',
                                         headers=self.get_standard_post_header(token))

        self.assertEqual("500 No article has been treated", response.status)
