"""
Make sure the UI widgets are configured correctly and work as expected.
"""
from PyQt5.QtWidgets import QLineEdit, QWidget, QApplication
from securedrop_client.gui.widgets import (ToolBar, MainView, SourceList,
                                           SourceWidget, LoginView)
from unittest import mock


app = QApplication([])


def test_ToolBar_init():
    """
    Ensure the ToolBar instance is correctly set up.
    """
    tb = ToolBar(None)
    assert "Logged out." in tb.user_state.text()


def test_ToolBar_setup():
    """
    Calling setup with references to a window and controller object results in
    them becoming attributes of self.
    """
    tb = ToolBar(None)
    mock_window = mock.MagicMock()
    mock_controller = mock.MagicMock()
    tb.setup(mock_window, mock_controller)
    assert tb.window == mock_window
    assert tb.controller == mock_controller


def test_ToolBar_set_logged_in_as():
    """
    Given a username, the user_state is updated and login/logout buttons are
    in the correct state.
    """
    tb = ToolBar(None)
    tb.user_state = mock.MagicMock()
    tb.login = mock.MagicMock()
    tb.logout = mock.MagicMock()
    tb.set_logged_in_as('test')
    tb.user_state.setText.assert_called_once_with('Logged in as: test')
    tb.login.setVisible.assert_called_once_with(False)
    tb.logout.setVisible.assert_called_once_with(True)


def test_ToolBar_set_logged_out():
    """
    Ensure the UI reverts to the logged out state.
    """
    tb = ToolBar(None)
    tb.user_state = mock.MagicMock()
    tb.login = mock.MagicMock()
    tb.logout = mock.MagicMock()
    tb.set_logged_out()
    tb.user_state.setText.assert_called_once_with('Logged out.')
    tb.login.setVisible.assert_called_once_with(True)
    tb.logout.setVisible.assert_called_once_with(False)


def test_ToolBar_on_login_clicked():
    """
    When login button is clicked, the window activates the login form.
    """
    tb = ToolBar(None)
    tb.window = mock.MagicMock()
    tb.on_login_clicked()
    tb.window.show_login.assert_called_once_with()


def test_ToolBar_on_logout_clicked():
    """
    When logout is clicked, the logout logic from the controller is started.
    """
    tb = ToolBar(None)
    tb.controller = mock.MagicMock()
    tb.on_logout_clicked()
    tb.controller.logout.assert_called_once_with()


def test_MainView_init():
    """
    Ensure the MainView instance is correctly set up.
    """
    mv = MainView(None)
    assert isinstance(mv.source_list, SourceList)
    assert isinstance(mv.filter_term, QLineEdit)
    assert isinstance(mv.view_holder, QWidget)


def test_MainView_update_view():
    """
    Ensure the passed-in widget is added to the layout of the main view holder
    (i.e. that area of the screen on the right hand side).
    """
    mv = MainView(None)
    mv.view_layout = mock.MagicMock()
    mock_widget = mock.MagicMock()
    mv.update_view(mock_widget)
    mv.view_layout.takeAt.assert_called_once_with(0)
    mv.view_layout.addWidget.assert_called_once_with(mock_widget)


def test_SourceList_update():
    """
    Check the items in the source list are cleared and a new SourceWidget for
    each passed-in source is created along with an associated QListWidgetItem.
    """
    sl = SourceList()
    sl.clear = mock.MagicMock()
    sl.addItem = mock.MagicMock()
    sl.setItemWidget = mock.MagicMock()
    mock_sw = mock.MagicMock()
    mock_lwi = mock.MagicMock()
    with mock.patch('securedrop_client.gui.widgets.SourceWidget', mock_sw), \
            mock.patch('securedrop_client.gui.widgets.QListWidgetItem',
                       mock_lwi):
        sources = ['a', 'b', 'c', ]
        sl.update(sources)
        sl.clear.assert_called_once_with()
        assert mock_sw.call_count == len(sources)
        assert mock_lwi.call_count == len(sources)
        assert sl.addItem.call_count == len(sources)
        assert sl.setItemWidget.call_count == len(sources)


def test_SourceWidget_init():
    """
    The source widget is initialised with the passed-in source.
    """
    mock_source = mock.MagicMock()
    mock_source.journalist_designation = 'foo bar baz'
    sw = SourceWidget(None, mock_source)
    assert sw.source == mock_source


def test_SourceWidget_update_starred():
    """
    Ensure the widget displays the expected details from the source.
    """
    mock_source = mock.MagicMock()
    mock_source.journalist_designation = 'foo bar baz'
    mock_source.is_starred = True
    sw = SourceWidget(None, mock_source)
    sw.name = mock.MagicMock()
    with mock.patch('securedrop_client.gui.widgets.load_svg') as mock_load:
        sw.update()
        mock_load.assert_called_once_with('star_on.svg')
    sw.name.setText.assert_called_once_with('<strong>foo bar baz</strong>')


def test_SourceWidget_update_unstarred():
    """
    Ensure the widget displays the expected details from the source.
    """
    mock_source = mock.MagicMock()
    mock_source.journalist_designation = 'foo bar baz'
    mock_source.is_starred = False
    sw = SourceWidget(None, mock_source)
    sw.name = mock.MagicMock()
    with mock.patch('securedrop_client.gui.widgets.load_svg') as mock_load:
        sw.update()
        mock_load.assert_called_once_with('star_off.svg')
    sw.name.setText.assert_called_once_with('<strong>foo bar baz</strong>')


def test_LoginView_init():
    """
    The LoginView is correctly initialised.
    """
    mock_controller = mock.MagicMock()
    lv = LoginView(None, mock_controller)
    assert lv.controller == mock_controller
    assert lv.title.text() == '<h1>Sign In</h1>'


def test_LoginView_reset():
    """
    Ensure the state of the login view is returned to the correct state.
    """
    mock_controller = mock.MagicMock()
    lv = LoginView(None, mock_controller)
    lv.username_field = mock.MagicMock()
    lv.password_field = mock.MagicMock()
    lv.tfa_field = mock.MagicMock()
    lv.setDisabled = mock.MagicMock()
    lv.error_label = mock.MagicMock()
    lv.reset()
    lv.username_field.setText.assert_called_once_with('')
    lv.password_field.setText.assert_called_once_with('')
    lv.tfa_field.setText.assert_called_once_with('')
    lv.setDisabled.assert_called_once_with(False)
    lv.error_label.setText.assert_called_once_with('')


def test_LoginView_error():
    """
    Any error message passed in is assigned as the text for the error label.
    """
    mock_controller = mock.MagicMock()
    lv = LoginView(None, mock_controller)
    lv.error_label = mock.MagicMock()
    lv.error('foo')
    lv.error_label.setText.assert_called_once_with('foo')


def test_LoginView_validate_no_input():
    """
    If the user doesn't provide input, tell them and give guidance.
    """
    mock_controller = mock.MagicMock()
    lv = LoginView(None, mock_controller)
    lv.username_field.text = mock.MagicMock(return_value='')
    lv.password_field.text = mock.MagicMock(return_value='')
    lv.tfa_field.text = mock.MagicMock(return_value='')
    lv.setDisabled = mock.MagicMock()
    lv.error = mock.MagicMock()
    lv.validate()
    assert lv.setDisabled.call_count == 2
    assert lv.error.call_count == 1


def test_LoginView_validate_input_non_numeric_2fa():
    """
    If the user doesn't provide numeric 2fa input, tell them and give
    guidance.
    """
    mock_controller = mock.MagicMock()
    lv = LoginView(None, mock_controller)
    lv.username_field.text = mock.MagicMock(return_value='foo')
    lv.password_field.text = mock.MagicMock(return_value='bar')
    lv.tfa_field.text = mock.MagicMock(return_value='baz')
    lv.setDisabled = mock.MagicMock()
    lv.error = mock.MagicMock()
    lv.validate()
    assert lv.setDisabled.call_count == 2
    assert lv.error.call_count == 1
    assert mock_controller.login.call_count == 0


def test_LoginView_validate_input_ok():
    """
    Valid input from the user causes a call to the controller's login method.
    """
    mock_controller = mock.MagicMock()
    lv = LoginView(None, mock_controller)
    lv.username_field.text = mock.MagicMock(return_value='foo')
    lv.password_field.text = mock.MagicMock(return_value='bar')
    lv.tfa_field.text = mock.MagicMock(return_value='123456')
    lv.setDisabled = mock.MagicMock()
    lv.error = mock.MagicMock()
    lv.validate()
    assert lv.setDisabled.call_count == 1
    assert lv.error.call_count == 0
    mock_controller.login.assert_called_once_with('foo', 'bar', '123456')
