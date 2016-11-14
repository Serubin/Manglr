
class UrlItem extends React.Component {

    aliasList = this.props.aliases.map((alias) =>
        <AliasItem urlId={this.props.urlId} alias={alias} />
    );

    constructor(props) {
        super(props)
        this.state = {
            is_open: false
        }
    }

    deleteElement() {
        //TODO ajax delete call
    }

    render() {
        
        return (
            <div>
                <tr id={ this.props.urlId + "-row" }>
                    <td>{this.props.urlId}</td>
                    <td>{this.props.url}</td>
                    <td className="actions">
                        <button type="button" className="btn btn-secondary" aria-label="Expand" onClick={this.toggleExpand}>
                            <i class="fa fa-angle-down" aria-hidden="true"></i>
                        </buttom>
                        <button type="button" className="btn btn-danger" aria-label="Delete" onClick={this.deleteElement}>
                            Delete
                        </button>
                    </td>
                </tr>
                <tr id={ this.props.urlId + "-aliases" }>
                    <ul>
                        {aliasList}
                    <ul>
                </tr>
            </div>
        );
    }
}
