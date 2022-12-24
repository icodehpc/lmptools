add_executable(lmptoolstests ${ALLTESTS})
target_link_libraries(lmptoolstests lmptools GTest::gtest GTest::gtest_main)
add_test(LMPTOOLSTestSuite lmptoolstests)
