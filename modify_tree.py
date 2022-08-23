import ast
from tree_util import get_node,get_model_name

def modify_tree(tree,parentDir,fileName):
    fitNode = get_node("fit", tree)
    evalNode =  get_node("evaluate", tree)
    fitNode = ast.Assign([ast.Name('history',ast.Store())],fitNode)
    evalNode = ast.Assign([ast.Name('eval_history',ast.Store())],evalNode)
    modelName = get_model_name(tree)

    startNameNode = ast.Name('start', ast.Store())
    endNameNode = ast.Name('end',ast.Store())
    callNode = ast.Call(ast.Name('time.time',ast.Load()),[],[])
    startExprNode = ast.Expr(ast.Assign([startNameNode],callNode))
    endExprNode = ast.Expr(ast.Assign([endNameNode],callNode))

    #model_benchmarks = {'model_name': [], 'num_model_params': [], 'validation_accuracy': [], 'acc_history': [], 'loss_history': [], 'time': [], 'eval_accuracy': [], 'eval_time': [], 'crash': []}
    benchmarkNameNode = ast.Name('model_benchmarks', ast.Store())
    benchmarkDictNode = ast.Dict()
    benchmarkNode = ast.Assign()
    property_list = ["model_name","num_model_params","train_time","crash","eval_time","validation_accuracy","accuracy_history","loss_history","eval_accuracy","val_loss_history","val_accuracy_history"]
    constNodeList = []
    listNodeList = []
    for x in range(len(property_list)):    
        listNode = ast.List()
        listNode.elts = []
        listNode.ctx = ast.Load()
        constNode = ast.Constant()
        constNode.value = property_list[x]
        listNodeList.append(listNode)
        constNodeList.append(constNode)
    targetList = []
    targetList.append(benchmarkNameNode)
    benchmarkDictNode.keys = constNodeList
    benchmarkDictNode.values = listNodeList
    benchmarkNode.targets = targetList
    benchmarkNode.value = benchmarkDictNode

    #model_benchmarks['train_time'].append(end-start)
    def getTimeRecordNode(property_name):
        subscriptNode = ast.Subscript()
        subscriptNode.value = benchmarkNameNode
        subscriptNode.slice = ast.Constant(property_name)
        subscriptNode.ctx = ast.Load()
        subtractNode = ast.BinOp()
        subtractNode.left = ast.Name('end',ctx=ast.Load())
        subtractNode.op = ast.Sub()
        subtractNode.right = ast.Name('start', ctx=ast.Load())
        timeRecordAttributeNode = ast.Attribute()
        timeRecordAttributeNode.value = subscriptNode
        timeRecordAttributeNode.attr = 'append'
        timeRecordAttributeNode.ctx = ast.Load()
        timeRecordCallNode = ast.Call(timeRecordAttributeNode,[subtractNode],[])
        timeRecordExprNode = ast.Expr()
        timeRecordExprNode.value = timeRecordCallNode
        return timeRecordExprNode

    #benchmark_df = pd.DataFrame(model_benchmarks)
    def getDataFrameNode():
        nameNode = ast.Name('benchmark_df',ctx=ast.Store())
        argNameNode = ast.Name('model_benchmarks',ctx=ast.Load())
        attributeNode = ast.Attribute()
        attributeNode.value = ast.Name('pd',ctx=ast.Load())
        attributeNode.attr = 'DataFrame'
        attributeNode.ctx = ast.Load()
        callNode = ast.Call(attributeNode,[argNameNode],[])
        assignNode = ast.Assign()
        assignNode.targets = [nameNode]
        assignNode.value = callNode
        return assignNode

    #benchmark_df.to_csv('benchmark_df.csv', index=False)
    def getCsvNode():
        attributeNode = ast.Attribute()
        attributeNode.value = ast.Name('benchmark_df',ctx=ast.Load())
        attributeNode.attr = 'to_csv'
        attributeNode.ctx = ast.Load()
        keywordNode = ast.keyword()
        keywordNode.arg = 'index'
        keywordNode.value = ast.Constant(False)
        callNode = ast.Call(attributeNode,[ast.Constant('benchmark_df_'+parentDir+'.csv')],[keywordNode])
        exprNode = ast.Expr(callNode)
        return exprNode

    #model_benchmarks['crash'].append('1')
    def getCrashNode():
        subscriptNode = ast.Subscript()
        subscriptNode.value = benchmarkNameNode
        subscriptNode.slice = ast.Constant('crash')
        subscriptNode.ctx = ast.Load()
        attributeNode = ast.Attribute()
        attributeNode.value = subscriptNode
        attributeNode.attr = 'append'
        attributeNode.ctx = ast.Load()
        callNode = ast.Call(attributeNode,[ast.Name('e',ctx=ast.Load())],[])
        exprNode = ast.Expr()
        exprNode.value = callNode
        return exprNode

        #model_benchmarks['crash'].append(' ')
    def getEmptyNode(name):
        subscriptNode = ast.Subscript()
        subscriptNode.value = benchmarkNameNode
        subscriptNode.slice = ast.Constant(name)
        subscriptNode.ctx = ast.Load()
        attributeNode = ast.Attribute()
        attributeNode.value = subscriptNode
        attributeNode.attr = 'append'
        attributeNode.ctx = ast.Load()
        callNode = ast.Call(attributeNode,[ast.Constant("-")],[])
        exprNode = ast.Expr()
        exprNode.value = callNode
        return exprNode

    # model_benchmarks['validation_accuracy'].append(history.history['val_accuracy'][-1])
    def getValidationAccuracyNode():
        subscriptNode = ast.Subscript()
        subscriptNode.value = benchmarkNameNode
        subscriptNode.slice = ast.Constant('validation_accuracy')
        subscriptNode.ctx = ast.Load()
        attributeNode = ast.Attribute()
        attributeNode.value = subscriptNode
        attributeNode.attr = 'append'
        attributeNode.ctx = ast.Load()
        secondSubscriptNode = ast.Subscript()
        secondAttributeNode = ast.Attribute()
        secondAttributeNode.value = ast.Name('history',ctx=ast.Load())
        secondAttributeNode.attr = 'history'
        secondAttributeNode.ctx = ast.Load()
        secondSubscriptNode.value = secondAttributeNode
        secondSubscriptNode.slice = ast.Constant("val_accuracy")
        secondSubscriptNode.ctx = ast.Load()
        callNode = ast.Call(attributeNode,[secondSubscriptNode],[])
        exprNode = ast.Expr()
        exprNode.value = callNode
        return exprNode

    # model_benchmarks['acc_history'].append(history.history['accuracy'])
    # model_benchmarks['loss_history'].append(history.history['loss'])
    def getHistoryNode(name):
        subscriptNode = ast.Subscript()
        subscriptNode.value = benchmarkNameNode
        subscriptNode.slice = ast.Constant(name+'_history')
        subscriptNode.ctx = ast.Load()
        attributeNode = ast.Attribute()
        attributeNode.value = subscriptNode
        attributeNode.attr = 'append'
        attributeNode.ctx = ast.Load()
        secondSubscriptNode = ast.Subscript()
        secondAttributeNode = ast.Attribute()
        secondAttributeNode.value = ast.Name('history',ctx=ast.Load())
        secondAttributeNode.attr = 'history'
        secondAttributeNode.ctx = ast.Load()
        secondSubscriptNode.value = secondAttributeNode
        secondSubscriptNode.slice = ast.Constant(name)
        secondSubscriptNode.ctx = ast.Load()
        callNode = ast.Call(attributeNode,[secondSubscriptNode],[])
        exprNode = ast.Expr()
        exprNode.value = callNode
        return exprNode

    # model_benchmarks['eval_accuracy'].append(eval_history)
    def getEvalAccuracyNode():
        subscriptNode = ast.Subscript()
        subscriptNode.value = benchmarkNameNode
        subscriptNode.slice = ast.Constant('eval_accuracy')
        subscriptNode.ctx = ast.Load()
        attributeNode = ast.Attribute()
        attributeNode.value = subscriptNode
        attributeNode.attr = 'append'
        attributeNode.ctx = ast.Load()
        callNode = ast.Call(attributeNode,[ast.Name('eval_history',ctx=ast.Load())],[])
        exprNode = ast.Expr()
        exprNode.value = callNode
        return exprNode

    # sys.exit()
    def getExitNode():
        attributeNode = ast.Attribute()
        attributeNode.value = ast.Name('sys',ctx=ast.Load())
        attributeNode.attr = 'exit'
        attributeNode.ctx = ast.Load()
        callNode = ast.Call(attributeNode,[],[])
        exprNode = ast.Expr()
        exprNode.value = callNode
        return exprNode

    # model_benchmarks['num_model_params'].append(model.count_params())
    def getNumParamNode():
        subscriptNode = ast.Subscript()
        subscriptNode.value = benchmarkNameNode
        subscriptNode.slice = ast.Constant('num_model_params')
        subscriptNode.ctx = ast.Load()
        attributeNode = ast.Attribute()
        attributeNode.value = subscriptNode
        attributeNode.attr = 'append'
        attributeNode.ctx = ast.Load()
        subAttributeNode = ast.Attribute()
        subAttributeNode.value = ast.Name(modelName,ctx=ast.Load())
        subAttributeNode.attr = 'count_params'
        subAttributeNode.ctx = ast.Load()
        subCallNode = ast.Call(subAttributeNode,[],[])
        callNode =ast.Call(attributeNode, [subCallNode],[])
        exprNode = ast.Expr()
        exprNode.value = callNode
        return exprNode

    # model_benchmarks['model_name'].append(name of model)
    def getModelNameNode(name):
        subscriptNode = ast.Subscript()
        subscriptNode.value = benchmarkNameNode
        subscriptNode.slice = ast.Constant(name)
        subscriptNode.ctx = ast.Load()
        attributeNode = ast.Attribute()
        attributeNode.value = subscriptNode
        attributeNode.attr = 'append'
        attributeNode.ctx = ast.Load()
        callNode = ast.Call(attributeNode,[ast.Constant(fileName[:-3]+"_"+parentDir)],[])
        exprNode = ast.Expr()
        exprNode.value = callNode
        return exprNode

    modelNameNode = getModelNameNode("model_name")
    csvNode = getCsvNode()
    dataFrameNode = getDataFrameNode()
    trainTimeRecordExprNode = getTimeRecordNode("train_time")
    evalTimeRecordExprNode = getTimeRecordNode("eval_time")
    crashNode = getCrashNode()
    valAccuracyNode = getValidationAccuracyNode()
    accHistoryNode = getHistoryNode("accuracy")
    lossHistoryNode = getHistoryNode("loss")
    valLossHistoryNode = getHistoryNode("val_loss")
    valAccuracyHistoryNode= getHistoryNode("val_accuracy")
    evalAccuracyNode = getEvalAccuracyNode()
    numParamNode = getNumParamNode()
    exitNode = getExitNode()

    #empty nodes
    emptyCrashNode = getEmptyNode("crash")
    emptyTrainTimeNode = getEmptyNode("train_time")
    emptyValAccuracyNode = getEmptyNode("validation_accuracy")
    emptyAccHistoryNode = getEmptyNode("accuracy_history")
    emptyLossHistoryNode = getEmptyNode("loss_history")
    emptyEvalAccuracyNode = getEmptyNode("eval_accuracy")
    emptyEvalTimeNode = getEmptyNode("eval_time")
    emptyValLossNode = getEmptyNode("val_loss_history")
    emptyValAccHistoryNode =getEmptyNode("val_accuracy_history")
    emptyNumParamNode = getEmptyNode("num_model_params")
    #except node
    except_handler = ast.ExceptHandler(type=ast.Name(id='Exception',ctx=ast.Load()),
                                           name='e',
                                           body=[benchmarkNode,modelNameNode,crashNode,emptyTrainTimeNode,emptyValAccuracyNode,emptyAccHistoryNode,
                                           emptyLossHistoryNode,emptyValLossNode,emptyNumParamNode,emptyValAccHistoryNode,emptyEvalAccuracyNode,emptyEvalTimeNode,dataFrameNode,csvNode,exitNode])
    for node in ast.walk(tree):
        if isinstance(node,ast.Attribute):
            if(node.attr=='compile'):
                tryNode = ast.Try(body=[benchmarkNode,modelNameNode,startExprNode,fitNode,endExprNode,trainTimeRecordExprNode,startExprNode,evalNode,endExprNode,
                evalTimeRecordExprNode,valAccuracyNode,accHistoryNode,numParamNode,lossHistoryNode,evalAccuracyNode,valLossHistoryNode,valAccuracyHistoryNode,emptyCrashNode,dataFrameNode,csvNode,exitNode],handlers=[except_handler],orelse=[],finalbody=[])
                tree.body.insert(node.lineno,tryNode)
                # tree.body.insert(node.lineno-1,benchmarkNode)

    ast.fix_missing_locations(tree)
    return tree

def add_imports(tree):
    #imports
    pdImport = ast.Import(names=[ast.alias(name='pandas',asname='pd')])
    tree.body.insert(0,pdImport)
    sysImport = ast.Import(names=[ast.alias(name='sys')])
    tree.body.insert(0,sysImport)
    timeImport = ast.Import(names=[ast.alias(name='time')])
    tree.body.insert(0,timeImport)
    return tree