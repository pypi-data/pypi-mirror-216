import logging


class FieldTest:
    @classmethod
    def simple_field_test(cls, field, db_value, internal_value, display_values):
        field.validate(None)
        # Test suite 1: Test Value Forms
        logging.info("Testing internal value to db value")
        assert field.to_db(internal_value) == db_value
        logging.info("Testing db value to internal value")
        assert field.from_db(db_value) == internal_value
        logging.info("Testing display value to internal value")
        for value in display_values:
            assert field.from_display(value) == internal_value
        logging.info("Testing internal value to display value")
        assert field.to_display(internal_value) in display_values
        logging.info("Testing guess internal value")
        assert field.guess_value(internal_value) == internal_value
        # Test suite 2: Pass test
        logging.info("Testing passthrough to db value")
        assert field.to_db(db_value) == db_value
        logging.info("Testing passthrough from db value")
        assert field.from_db(internal_value) == internal_value
        logging.info("Testing passthrough from display value")
        assert field.from_display(internal_value) == internal_value
        logging.info("Testing passthrough to display value")
        for value in display_values:
            assert field.to_display(value) in display_values
        # Test suite 3: Test None management
        logging.info("Testing None to db value")
        assert field.to_db(None) is None
        logging.info("Testing None from db value")
        assert field.from_db(None) is None
        logging.info("Testing None get value")
        assert field.get_value(None) is None
        logging.info("Testing None from display value")
        assert field.from_display(None) is None
        logging.info("Testing None to display value")
        assert field.to_display(None) is None
        # Test suite 4: sample value management
        logging.info("Testing Sample value generation")
        if field.internal_form:  # Some field has no fixed internal
            logging.info("Testing Sample value infernal value type")
            assert isinstance(field.sample, field.internal_form)
        logging.info("Testing Sample value to_db from_db routine")
        assert field.from_db(field.to_db(field.sample)) == field.sample
        logging.info("Testing Sample value to_display from_display routine")
        assert field.from_display(field.to_display(field.sample)) == field.sample

    @classmethod
    def runtime_field_test(cls, field, db_value, internal_value, runtime_value, display_value, detail_value,
                           none_value=None):
        # Test suite 1: Test Value Forms
        logging.info("Testing db value to internal value")
        assert field.from_db(db_value) == internal_value
        logging.info("Testing internal value to db value")
        assert field.to_db(internal_value) == db_value
        logging.info("Testing internal value to display value")
        assert field.to_display(internal_value) == (display_value, none_value)
        logging.info("Testing internal value to get runtime value")
        assert field.get_value(internal_value) == (internal_value, runtime_value)
        logging.info("Testing display value to internal value")
        assert field.from_display(display_value, detail_value) == (internal_value, runtime_value)
        logging.info("Testing runtime value to internal value")
        assert field.from_runtime(runtime_value) == internal_value
        logging.info("Testing display value to internal value")
        assert field.from_display(display_value, none_value) == (internal_value, none_value)
        logging.info("Testing guess internal value")
        assert field.guess_value(internal_value) == (internal_value, none_value)
        logging.info("Testing guess internal value")
        assert field.guess_value(display_value) == (internal_value, none_value)
        logging.info("Testing guess detail value")
        assert field.guess_value(detail_value) == (internal_value, runtime_value)
        # Test suite 2: Pass test
        logging.info("Testing passthrough from db value")
        assert field.from_db(internal_value) == internal_value
        logging.info("Testing passthrough to db value")
        assert field.to_db(db_value) == db_value
        logging.info("Testing passthrough to display value")
        assert field.to_display(display_value) == (display_value, none_value)
        logging.info("Testing passthrough to display value with detail value")
        assert field.to_display(display_value, detail_value) == (display_value, detail_value)
        logging.info("Testing passthrough get value with runtime value")
        assert field.get_value(internal_value, runtime_value) == (internal_value, runtime_value)
        logging.info("Testing passthrough from display value with runtime")
        assert field.from_display(internal_value, runtime_value) == (internal_value, runtime_value)
        logging.info("Testing passthrough from display value without runtime")
        assert field.from_display(internal_value) == (internal_value, none_value)
        # Test suite 3: Test None management
        logging.info("Testing None to db value")
        assert field.to_db(None) is None
        logging.info("Testing None from db value")
        assert field.from_db(None) is None
        logging.info("Testing None get value")
        assert field.get_value(None) == (None, None)
        logging.info("Testing None from display value")
        assert field.from_display(None) == (None, None)
        logging.info("Testing None to display value")
        assert field.to_display(None) == (None, None)
        # Test suite 4: sample value management
        logging.info("Testing Sample value generation")
        if field.internal_form:  # Some field has no fixed internal form
            logging.info("Testing Sample value infernal value type")
            assert isinstance(field.sample[0], field.internal_form)
        if field.runtime_form:  # Some field has no fixed runtime form
            logging.info("Testing Sample value runtime value type")
            assert isinstance(field.sample[1], field.runtime_form)
        logging.info("Testing Sample value to_db from_db routine")
        assert field.from_db(field.to_db(*field.sample)) == field.sample[0]
        logging.info("Testing Sample value to_display from_display routine")
        assert field.from_display(*field.to_display(*field.sample)) == field.sample
