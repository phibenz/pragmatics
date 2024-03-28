DIFFICULTIES = ["easy", "medium", "hard"]
METADATA_KEYS = ["blog", "reference", "arxiv"]


class TemplateTest:
    def __init__(self, template_dict):
        self.template_dict = template_dict

    def test_template(self):
        # Test the template
        self._check_id()
        self._check_info()
        if "query" in self.template_dict:
            self._check_query(self.template_dict["query"])

    def _check_id(self):
        assert "id" in self.template_dict, "Template ID is missing"
        assert self.template_dict["id"] is not None, "Template ID is missing"
        template_id = self.template_dict["id"]
        assert isinstance(template_id, str), "Template ID should be a string"
        assert len(template_id) > 0, "Template ID should not be empty"
        assert " " not in template_id, "Template ID should not contain spaces"

    def _check_info(self):
        assert "info" in self.template_dict, "Template info is missing"
        assert self.template_dict["info"] is not None, "Template info is missing"
        info = self.template_dict["info"]
        assert isinstance(info, dict), "Template info should be a dictionary"
        # Mandatory keys
        self._check_info_name(info)
        self._check_info_author(info)
        self._check_info_difficulty(info)
        self._check_info_description(info)
        self._check_info_tags(info)
        if "metadata" in info:
            self._check_info_metadata(info["metadata"])

    def _check_info_name(self, info):
        assert "name" in info, "Template info name key is missing"
        assert info["name"] is not None, "Template info name value is missing"
        info_name = info["name"]
        assert isinstance(info_name, str), "Template name should be a string"
        assert len(info_name) > 0, "Template name should not be empty"

    def _check_info_author(self, info):
        assert "author" in info, "Template info author key is missing"
        assert info["author"] is not None, "Template info author value is missing"
        author = info["author"]
        assert isinstance(author, str), "Template author should be a string"
        assert len(author) > 0, "Template author should not be empty"

    def _check_info_difficulty(self, info):
        assert "difficulty" in info, "Template info difficulty key is missing"
        assert (
            info["difficulty"] is not None
        ), "Template info difficulty value is missing"
        difficulty = info["difficulty"]
        assert isinstance(difficulty, str), "Template difficulty should be a string"
        assert (
            difficulty in DIFFICULTIES
        ), "Template difficulty should be easy, medium, or hard"

    def _check_info_description(self, info):
        assert "description" in info, "Template info description key is missing"
        assert (
            info["description"] is not None
        ), "Template info description value is missing"
        description = info["description"]
        assert isinstance(description, str), "Template description should be a string"
        assert len(description) > 0, "Template description should not be empty"

    def _check_info_tags(self, info):
        assert "tags" in info, "Template info tags key is missing"
        assert info["tags"] is not None, "Template info tags value is missing"
        tags = info["tags"]
        assert isinstance(tags, list), "Template tags should be a list"
        assert len(tags) > 0, "Template tags should not be empty"
        for tag in tags:
            assert isinstance(tag, str), "Template tag should be a string"
            assert len(tag) > 0, "Template tag should not be empty"
            assert tag == tag.lower(), "Template tag should be lowercase"

    def _check_info_metadata(self, metadata):
        assert isinstance(metadata, dict), "Template metadata should be a dictionary"
        for key in metadata:
            if key not in METADATA_KEYS:
                assert False, f"Template metadata key {key} is not recognized"
        for key in METADATA_KEYS:
            if key in metadata:
                assert isinstance(
                    metadata[key], str
                ), f"Template {key} should be a string"
                assert len(metadata[key]) > 0, f"Template {key} should not be empty"

    def _check_query(self, query):
        assert isinstance(query, dict), "Template query should be a dictionary"
        pass
