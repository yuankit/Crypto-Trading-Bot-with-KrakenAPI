# URL path elements for authenticated endpoints
USER_DATA = {
    'GET_ACCOUNT_BALANCE': '/0/private/Balance',
    'GET_TRADE_BALANCE': '/0/private/TradeBalance',
    'GET_OPEN_ORDERS': '/0/private/OpenOrders',
    'GET_CLOSED_ORDERS': '/0/private/ClosedOrders',
    'QUERY_ORDERS_INFO': '/0/private/QueryOrders',
    'GET_TRADES_HISTORY': '/0/private/TradesHistory',
    'QUERY_TRADES_INFO': '/0/private/QueryTrades',
    'GET_OPEN_POSITIONS': '/0/private/OpenPositions',
    'GET_LEDGERS_INFO': '/0/private/Ledgers',
    'QUERY_LEDGERS': '/0/private/QueryLedgers',
    'GET_TRADE_VOLUME': '/0/private/TradeVolume',
    'REQUEST_EXPORT_REPORT': '/0/private/AddExport',
    'GET_EXPORT_REPORT_STATUS': '/0/private/ExportStatus',
    'RETRIEVE_DATA_EXPORT': '/0/private/RetrieveExport',
    'DELETE_EXPORT_REPORT': '/0/private/RemoveExport'
}

USER_TRADING = {
    'ADD_ORDER': '/0/private/AddOrder',
    'CANCEL_ORDER': '/0/private/CancelOrder',
    'CANCEL_ALL_ORDERS': '/0/private/CancelAll',
    'CANCEL_ALL_ORDERS_AFTER_X': '/0/private/CancelAllOrdersAfter' 
}

USER_FUNDING = {
    'GET_DEPOSIT_METHODS': '/0/private/DepositMethods',
    'GET_DEPOSIT_ADDRESSES': '/0/private/DepositAddresses',
    'GET_STATUS_OF_RECENT_DEPOSITS': '/0/private/DepositStatus',
    'GET_WITHDRAWAL_INFORMATION': '/0/private/WithdrawInfo',
    'WITHDRAW_FUNDS': '/0/private/Withdraw',
    'GET_STATUS_OF_RECENT_WITHDRAWALS': '/0/private/WithdrawStatus',
    'REQUEST_WITHDRAWAL_CANCELATION': '/0/private/WithdrawCancel',
    'REQUEST_WALLET_TRANSFER': '/0/private/WalletTransfer'
}

USER_STAKING = {
    'STAKE_ASSET':'/0/private/Stake',
    'UNSTAKE_ASSET': '/0/private/Unstake',
    'LIST_OF_STAKEABLE_ASSETS': '/0/private/Staking/Assets',
    'GET_PENDING_STAKING_TRANSACTIONS': '/0/private/Staking/Pending',
    'LIST_OF_STAKING_TRANSACTIONS': '/0/private/Staking/Transactions'
}

WEBSOCKETS_AUTHENTICATION = {
    'GET_WEBSOCKETS_TOKEN': '/0/private/GetWebSocketsToken'
}

