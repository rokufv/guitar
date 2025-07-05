# test_agent_system.py
"""
RAG x Agentsシステムのテストスクリプト
"""

import os
import sys
from config import GOOGLE_API_KEY

def test_basic_functionality():
    """基本機能のテスト"""
    
    print("=== RAG x Agentsシステム テスト ===")
    print(f"Google API Key: {'設定済み' if GOOGLE_API_KEY else '未設定'}")
    
    if not GOOGLE_API_KEY:
        print("⚠️  環境変数GOOGLE_API_KEYが設定されていません。")
        return False
    
    try:
        # エージェントシステムのインポートテスト
        from agent_system import GuitarEquipmentAgent
        print("✅ エージェントシステムのインポート成功")
        
        # エージェントの初期化テスト
        agent = GuitarEquipmentAgent()
        print("✅ エージェントの初期化成功")
        
        # ツールのテスト
        print("\n=== ツールテスト ===")
        
        # サウンド特徴分析テスト
        result = agent._analyze_sound_characteristics("B'z 松本孝弘")
        print(f"サウンド特徴分析テスト: {len(result) > 0}")
        
        # カテゴリ検索テスト
        result = agent._search_equipment_by_category("B'z 松本孝弘|ギター")
        print(f"カテゴリ検索テスト: {len(result) > 0}")
        
        # 予算検索テスト
        result = agent._search_equipment_by_budget("B'z 松本孝弘|500000")
        print(f"予算検索テスト: {len(result) > 0}")
        
        print("\n✅ 基本機能テスト完了")
        return True
        
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        return False

def test_integration():
    """統合テスト"""
    
    print("\n=== 統合テスト ===")
    
    try:
        # RAGシステムとの統合テスト
        from rag_system import RAGSystem
        
        rag_system = RAGSystem()
        print("✅ RAGシステムの初期化成功")
        print(f"バージョン: {rag_system.version}")
        
        # エージェントベースのチェーン作成テスト
        chain = rag_system.create_rag_chain("B'z 松本孝弘", use_agent=True)
        print("✅ エージェントベースチェーン作成成功")
        
        # 標準チェーン作成テスト
        chain = rag_system.create_rag_chain("B'z 松本孝弘", use_agent=False)
        print("✅ 標準チェーン作成成功")
        
        print("\n✅ 統合テスト完了")
        return True
        
    except Exception as e:
        print(f"❌ 統合テストでエラーが発生しました: {e}")
        return False

def test_recommendation():
    """推薦システムテスト（実際のAPIを使用）"""
    
    print("\n=== 推薦システムテスト ===")
    
    try:
        from agent_system import GuitarEquipmentAgent
        
        agent = GuitarEquipmentAgent()
        
        # 簡単な推薦テスト
        print("推薦テストを実行中...")
        result = agent.recommend_equipment(
            guitarist="B'z 松本孝弘",
            budget=500000,
            equipment_type="ギター",
            user_query="ハードロックに最適なギターを推薦してください"
        )
        
        print(f"推薦結果の長さ: {len(result)} 文字")
        print(f"推薦結果の一部: {result[:200]}...")
        
        print("\n✅ 推薦システムテスト完了")
        return True
        
    except Exception as e:
        print(f"❌ 推薦システムテストでエラーが発生しました: {e}")
        return False

def main():
    """メイン関数"""
    
    print("RAG x Agentsシステム テストスイート")
    print("=" * 50)
    
    tests = [
        ("基本機能テスト", test_basic_functionality),
        ("統合テスト", test_integration),
        ("推薦システムテスト", test_recommendation),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{test_name}を実行中...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name}で予期しないエラー: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("テスト結果サマリー:")
    
    for test_name, result in results:
        status = "✅ 成功" if result else "❌ 失敗"
        print(f"{test_name}: {status}")
    
    success_count = sum(1 for _, result in results if result)
    total_count = len(results)
    
    print(f"\n成功: {success_count}/{total_count}")
    
    if success_count == total_count:
        print("🎉 すべてのテストが成功しました！")
    else:
        print("⚠️  一部のテストが失敗しました。")

if __name__ == "__main__":
    main() 