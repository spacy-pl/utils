from tqdm import tqdm


class Strategy:
    """This class represents a strategy for squashing tags from NKJP"""

    def __init__(self):
        pass

    def prepare_conversion(self, structured_data):
        """This function prepares data needed to convert nkjp tags to new tags

        :param structured_data: structured NKJP tagset (in format described below)

        :returns conversion_function, transitional_tagset
            where conversion_function is dict(<original_tag>: <new_tag>)
            and transitional_tagset is new tagset in structured tagset format

        Structured tagset format is:
            dict(<pos_tag/fleksem> : list(dict(
                'tags': [<other tags>],
                'card': <cardinality>,
            )), where things in '<>' brackets are variables.
        """
        raise NotImplementedError

    @staticmethod
    def make_full_tag(fleksem, tags):
        return fleksem + ":" + ":".join(tags) if tags else fleksem


class JustPOS(Strategy):

    def prepare_conversion(self, structured_data):
        conversion_map = {}
        transitional_tagset = {}

        num_subclasses = 0
        for subclasses in structured_data.values():
            num_subclasses += len(subclasses)

        with tqdm(total=num_subclasses) as pbar:
            for fleksem, subclasses in structured_data.items():
                fleksem_card = 0
                for subclass in subclasses:
                    conversion_map[self.make_full_tag(fleksem, subclass['tags'])] = fleksem
                    fleksem_card += subclass['card']
                    pbar.update(1)
                transitional_tagset[fleksem] = [{'tags': [], 'card': fleksem_card}]

        return conversion_map, transitional_tagset
