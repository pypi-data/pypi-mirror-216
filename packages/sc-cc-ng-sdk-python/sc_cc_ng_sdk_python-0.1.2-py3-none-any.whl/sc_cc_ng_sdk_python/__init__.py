from dataclasses import dataclass, asdict
from requests import post
from sc_cc_ng_models_python import ContextFilter, BitVal
from typing import List, Optional
from enum import Enum

@dataclass
class DictResult:

    """
        A result object, containing meta data if everything was ok else an error.
    """

    data:   Optional[List[dict]]    = None
    error:  Optional[str]           = None

@dataclass
class ListResult:

    """
        A result object, containing meta data if everything was ok else an error.
    """

    data:   Optional[List[BitVal]]  = None
    error:  Optional[str]           = None

@dataclass
class SCNG:

    url: str

    def to_dict(
        self, 
        tokens_list: List[List[str]],
        context_filter: Optional[ContextFilter] = None,
    ) -> DictResult:

        """
            Converts lists of tokens to a list of dictionaries, containing
            all matching meta data to those tokens. If no meta data was found
            for a combination of tokens, the dictionary will be empty.

            :param tokens_list: A list of lists of tokens.
            :param context_filter: A context filter object.

            :return: A result object.
        """
        try:
            if context_filter is None:
                context_filter = ContextFilter.empty()

            response = post(
                self.url,
                json={
                    "query": """
                        query TokenListDictQuery(
                            $tokenList: [[String!]!]!,
                            $contextFilter: ContextFilter,
                        ) {
                            tokensListBasedContentAsDict(
                                tokenList: $tokenList
                                contextFilter: $contextFilter
                            )
                        }
                    """,
                    "variables": {
                        "tokenList": tokens_list,
                        "contextFilter": context_filter.to_dict(),
                    }
                },
            )
            if response.status_code == 200:
                json = response.json()
                if "errors" in json:
                    return DictResult(error=json["errors"])
                else:
                    return DictResult(data=response.json()['data']['tokensListBasedContentAsDict'])
            else:
                return DictResult(error=response.text)
        except Exception as e:
            return DictResult(error=str(e))
    
    def to_list(
        self,
        tokens_list: List[List[str]],
        context_filter: Optional[ContextFilter] = None,
    ) -> ListResult:

        """
            Converts lists of tokens to a list of bit values, containing
            all matching meta data to those tokens. If no meta data was found
            for a combination of tokens, the list will be empty.

            :param tokens_list: A list of lists of tokens.
            :param context_filter: A context filter object.

            :return: A result object.
        """

        try:
            if context_filter is None:
                context_filter = ContextFilter.empty()

            response = post(
                self.url,
                json={
                    "query": """
                        query TokenListListQuery(
                            $tokenList: [[String!]!]!,
                            $contextFilter: ContextFilter,
                        ) {
                            tokenListBasedContent(
                                tokenList: $tokenList
                                contextFilter: $contextFilter
                            ) {
                                context
                                value
                            }
                        }
                    """,
                    "variables": {
                        "tokenList": tokens_list,
                        "contextFilter": context_filter.to_dict(),
                    }
                },
            )
            if response.status_code == 200:
                json = response.json()
                if "errors" in json:
                    return ListResult(error=json["errors"])
                else:
                    return ListResult(
                        data=list(
                            map(
                                lambda xs: list(
                                    map(
                                        lambda x: BitVal(
                                            context=x['context'],
                                            value=x['value'],
                                        ),
                                        xs
                                    )
                                ),
                                response.json()['data']['tokenListBasedContent']
                            )
                        )
                    )
            else:
                return ListResult(error=response.text)
        except Exception as e:
            return ListResult(error=str(e))

