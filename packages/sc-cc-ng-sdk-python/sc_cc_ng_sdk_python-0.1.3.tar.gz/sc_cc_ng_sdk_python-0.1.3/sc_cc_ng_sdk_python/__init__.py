from dataclasses import dataclass, asdict
from requests import post
from sc_cc_ng_models_python import ContextFilter, BitVal
from typing import List, Optional, Any
from enum import Enum

@dataclass
class Result:

    """
        A result object, containing data if everything was ok else an error.
    """

    data:   Optional[Any]   = None
    error:  Optional[str]   = None


@dataclass
class SCNG:

    url: str

    def to_dict_list(
        self, 
        tokens_list: List[List[str]],
        context_filter: Optional[ContextFilter] = None,
    ) -> Result:

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
                    return Result(error=json["errors"])
                else:
                    return Result(data=response.json()['data']['tokensListBasedContentAsDict'])
            else:
                return Result(error=response.text)
        except Exception as e:
            return Result(error=str(e))
    
    def to_bit_list(
        self,
        tokens_list: List[List[str]],
        context_filter: Optional[ContextFilter] = None,
    ) -> Result:

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
                                reason
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
                    return Result(error=json["errors"])
                else:
                    return Result(
                        data=list(
                            map(
                                lambda xs: list(
                                    map(
                                        lambda x: BitVal(
                                            context=x['context'],
                                            value=x['value'],
                                            reason=x['reason'],
                                        ),
                                        xs
                                    )
                                ),
                                response.json()['data']['tokenListBasedContent']
                            )
                        )
                    )
            else:
                return Result(error=response.text)
        except Exception as e:
            return Result(error=str(e))

    def to_string_list(
        self, 
        tokens_list: list,
        context_filter: Optional[ContextFilter] = None,
    ) -> Result:
            
        """
            Converts lists of tokens to a list of strings, containing
            all matching meta data to those tokens. If no meta data was found
            for a combination of tokens, the list will be empty.

            :param tokens_list: A list of lists of tokens.
            :param context_filter: A context filter object.

            :return: A result object.
        """

        try:
            internal_result = self.to_bit_list(
                tokens_list=tokens_list,
                context_filter=context_filter,
            )
            if internal_result.error is None:
                return Result(
                    data=list(
                        map(
                            lambda xs: list(
                                map(
                                    lambda x: x.to_string(),
                                    xs
                                )
                            ),
                            internal_result.data
                        )
                    )
                )
            else:
                return internal_result
        except Exception as e:
            return Result(error=str(e))
